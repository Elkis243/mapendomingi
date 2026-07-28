from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'page': 'MAPENDO MINGI'})


DOMAIN_PAGES = {
    'femme-enfant': {
        'page': 'Promotion de la Femme & Protection de l’Enfant',
        'hero_title': 'Promotion de la Femme & Protection de l’Enfant',
        'hero_image': 'images/promotion-femme-enfant.webp',
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


def blog(request):
    return render(request, 'blog.html', {'page': 'Blog'})


def donate(request):
    return render(request, 'donate.html', {'page': 'Faire un don'})


def contact(request):
    sent = False
    if request.method == 'POST':
        sent = True
    return render(request, 'contact.html', {'page': 'Contact', 'sent': sent})


def about(request):
    return render(request, 'about.html', {'page': 'Qui sommes-nous'})


def domain_detail(request, slug):
    domain = DOMAIN_PAGES.get(slug)
    if not domain:
        from django.http import Http404
        raise Http404("Domaine introuvable")
    return render(request, 'domain_detail.html', domain)
