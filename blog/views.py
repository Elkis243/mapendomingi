"""
Vues du blog : liste et détail des articles publiés.
"""

from django.db.models import F, Prefetch
from django.views.generic import DetailView, ListView

from .models import Post, PostImage


class PostListView(ListView):
    """Liste paginée des articles publiés, du plus récent au plus ancien."""

    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related("category", "author")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=PostImage.objects.order_by("order", "id"),
                )
            )
            .order_by("-published_at", "-created_at")
        )


class PostDetailView(DetailView):
    """
    Détail d'un article publié.

    Incrémente le compteur de vues une seule fois par session
    pour éviter les faux positifs liés au rafraîchissement.
    """

    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related("category", "author")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=PostImage.objects.order_by("order", "id"),
                )
            )
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self._increment_views_once_per_session()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def _increment_views_once_per_session(self):
        """Incrémente `views` uniquement lors de la première visite en session."""
        session_key = "blog_viewed_posts"
        viewed_posts = self.request.session.get(session_key, [])

        post_id = self.object.pk
        if post_id in viewed_posts:
            return

        Post.objects.filter(pk=post_id).update(views=F("views") + 1)
        # Recharger la valeur à jour pour le template
        self.object.refresh_from_db(fields=["views"])

        viewed_posts.append(post_id)
        self.request.session[session_key] = viewed_posts
        self.request.session.modified = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Galerie déjà préchargée et triée via Prefetch
        context["gallery"] = post.images.all()

        context["related_posts"] = (
            Post.objects.filter(
                status=Post.Status.PUBLISHED,
                category=post.category,
            )
            .exclude(pk=post.pk)
            .select_related("category", "author")
            .order_by("-published_at", "-created_at")[:3]
        )

        return context
