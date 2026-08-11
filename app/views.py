import logging
import re

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render

from app.brevo import BrevoError, send_transactional_email
from blog.models import Post

logger = logging.getLogger(__name__)

CONTACT_RATE_LIMIT = 3
CONTACT_RATE_WINDOW_SECONDS = 10 * 60
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or "unknown"


def _contact_rate_limited(request) -> bool:
    """True si l'IP a dépassé la limite d'envois contact."""
    cache_key = f"contact_rate:{_client_ip(request)}"
    count = cache.get(cache_key, 0)
    if count >= CONTACT_RATE_LIMIT:
        return True
    cache.set(cache_key, count + 1, CONTACT_RATE_WINDOW_SECONDS)
    return False


def _valid_contact_payload(data: dict) -> tuple[bool, dict]:
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not subject or not message:
        return False, {}
    if not EMAIL_PATTERN.match(email):
        return False, {}
    if len(name) > 120 or len(email) > 254 or len(subject) > 200 or len(message) > 5000:
        return False, {}

    return True, {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    }


def _send_contact_message(payload: dict) -> None:
    body = (
        "Nouveau message via le formulaire de contact\n\n"
        f"Nom : {payload['name']}\n"
        f"Email : {payload['email']}\n"
        f"Sujet : {payload['subject']}\n\n"
        f"Message :\n{payload['message']}\n"
    )
    send_transactional_email(
        to_email=settings.CONTACT_EMAIL_TO,
        subject=f"[Contact] {payload['subject']}",
        text_content=body,
        reply_to_email=payload["email"],
        reply_to_name=payload["name"],
        sender_name=settings.CONTACT_SENDER_NAME,
    )


def home(request):
    featured_posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("category", "author")
        .order_by("-is_featured", "-views", "-published_at", "-created_at")[:3]
    )
    return render(
        request,
        "home.html",
        {
            "page": "Mapendo Mingi",
            "featured_posts": featured_posts,
        },
    )


DOMAIN_PAGES = {
    'femme-enfant': {
        'page': 'Promotion de la Femme & Protection de l’Enfant',
        'hero_title': 'Promotion de la Femme & Protection de l’Enfant',
        'hero_image': 'images/promotion-femmes-enfants.webp',
        'og_image': 'images/og/femme-enfant.webp',
        'hero_alt': 'Femmes et enfants accompagnés par MAPENDO MINGI',
        'article_title': 'Un engagement pour la dignité et la protection',
        'paragraphs': [
            (
                "Nous plaçons la femme et l’enfant au coeur de nos priorités afin de "
                "défendre leurs droits, renforcer leur protection et soutenir leur place "
                "dans la société. À travers ce domaine, nous accompagnons les femmes "
                "confrontées à la précarité, aux violences ou à l’exclusion, tout en "
                "développant des actions de protection, d’écoute et de sensibilisation "
                "au bénéfice des enfants les plus vulnérables."
            ),
            (
                "Nous travaillons avec les familles, les leaders communautaires et les "
                "acteurs locaux pour prévenir les abus, promouvoir l’égalité et "
                "encourager un environnement plus sûr, plus digne et plus protecteur. "
                "Cette approche favorise une meilleure prise en charge des situations "
                "de fragilité, renforce la vigilance communautaire et valorise le rôle "
                "des femmes comme actrices majeures du changement social."
            ),
            (
                "Notre ambition est aussi de favoriser l’autonomisation des femmes, "
                "de restaurer la confiance des personnes vulnérables et de créer des "
                "opportunités durables pour celles et ceux qui ont le plus besoin "
                "d’accompagnement. En mettant l’accent sur la protection, l’écoute, "
                "l’information et la solidarité, nous voulons contribuer à bâtir des "
                "communautés où chaque femme et chaque enfant peut évoluer avec respect, "
                "sécurité et espoir."
            ),
        ],
    },
    'education-jeunesse': {
        'page': 'Éducation, Jeunesse & Entrepreneuriat',
        'hero_title': 'Éducation, Jeunesse & Entrepreneuriat',
        'hero_image': 'images/education-jeunesse-entrepreneur.webp',
        'og_image': 'images/og/education-jeunesse.webp',
        'hero_alt': 'Jeunes en situation d’apprentissage et d’accompagnement',
        'article_title': 'Former et ouvrir des perspectives',
        'paragraphs': [
            (
                "Nous croyons que l’éducation, l’accompagnement de la jeunesse et "
                "l’esprit d’initiative sont des leviers essentiels pour transformer "
                "durablement les communautés. Nos actions encouragent l’accès à "
                "l’apprentissage, le renforcement des capacités et l’orientation "
                "des jeunes vers des parcours porteurs d’avenir, en lien avec leurs "
                "talents et les réalités de leur environnement."
            ),
            (
                "Nous soutenons également les initiatives qui développent la "
                "créativité, le leadership, la confiance en soi et la capacité des "
                "jeunes à prendre part aux décisions qui façonnent leur futur. En "
                "misant sur l’encadrement, l’écoute et la valorisation des compétences, "
                "nous cherchons à faire émerger une jeunesse plus consciente, plus "
                "engagée et mieux préparée aux défis de demain."
            ),
            (
                "En valorisant l’entrepreneuriat et les projets à impact, nous "
                "aidons les jeunes à bâtir leur autonomie, à créer de la valeur et "
                "à contribuer activement au développement économique et social de leur "
                "communauté. À travers cette approche, nous souhaitons faire émerger "
                "une jeunesse engagée, compétente et confiante, capable d’innover, "
                "de collaborer et de devenir un véritable moteur de transformation locale."
            ),
        ],
    },
    'sante-durable': {
        'page': 'Santé & Développement Durable',
        'hero_title': 'Santé & Développement Durable',
        'hero_image': 'images/sante-developpement-durable.webp',
        'og_image': 'images/og/sante-durable.webp',
        'hero_alt': 'Initiatives communautaires pour la santé et le développement durable',
        'article_title': 'Prendre soin aujourd’hui, construire demain',
        'paragraphs': [
            (
                "La santé et le développement durable sont au centre de notre vision "
                "d’un avenir plus équilibré, plus résilient et plus humain. Nous "
                "encourageons des actions qui améliorent l’accès aux soins, renforcent "
                "la prévention, soutiennent le bien-être des familles et accompagnent "
                "les communautés vers de meilleures pratiques sanitaires."
            ),
            (
                "Nos interventions portent aussi sur la sensibilisation, l’hygiène, "
                "la santé communautaire et la promotion de comportements qui "
                "protègent durablement les personnes, en particulier les plus "
                "vulnérables. Cette démarche vise à réduire les risques, améliorer "
                "les conditions de vie quotidiennes et renforcer la capacité des "
                "communautés à faire face aux défis sanitaires."
            ),
            (
                "En parallèle, nous promouvons des approches durables qui préservent "
                "les ressources, valorisent les initiatives locales et contribuent à "
                "un développement respectueux des personnes et de leur milieu de vie. "
                "Notre démarche relie ainsi santé, environnement et résilience "
                "communautaire, afin d’aider les populations à vivre dans des "
                "conditions plus saines, plus stables et plus durables sur le long terme."
            ),
        ],
    },
}


def donate(request):
    return render(request, 'donate.html', {'page': 'Faire un don'})


def contact(request):
    sent = False
    rate_limited = False
    send_error = False
    if request.method == "POST":
        if _contact_rate_limited(request):
            rate_limited = True
        else:
            is_valid, payload = _valid_contact_payload(request.POST)
            if is_valid:
                try:
                    _send_contact_message(payload)
                    sent = True
                except BrevoError:
                    logger.exception("Échec d'envoi du formulaire de contact")
                    send_error = True
            else:
                send_error = True
    return render(
        request,
        "contact.html",
        {
            "page": "Contact",
            "sent": sent,
            "rate_limited": rate_limited,
            "send_error": send_error,
        },
    )


def about(request):
    return render(request, 'about.html', {'page': 'Qui sommes-nous'})


GALLERY_IMAGES = [
    {
        "src": "images/galeries/picture1.webp",
        "alt": "Actions de MAPENDO MINGI sur le terrain",
        "width": 700,
        "height": 463,
    },
    {
        "src": "images/galeries/picture2.webp",
        "alt": "Communauté accompagnée par MAPENDO MINGI",
        "width": 800,
        "height": 600,
    },
    {
        "src": "images/galeries/picture3.webp",
        "alt": "Moment de partage et de solidarité",
        "width": 800,
        "height": 600,
    },
    {
        "src": "images/galeries/picture4.webp",
        "alt": "Engagement communautaire de MAPENDO MINGI",
        "width": 700,
        "height": 525,
    },
]


def gallery(request):
    return render(
        request,
        "gallery.html",
        {
            "page": "Galerie",
            "gallery_images": GALLERY_IMAGES,
        },
    )


def domain_detail(request, slug):
    domain = DOMAIN_PAGES.get(slug)
    if not domain:
        from django.http import Http404
        raise Http404("Domaine introuvable")
    return render(request, 'domain_detail.html', domain)
