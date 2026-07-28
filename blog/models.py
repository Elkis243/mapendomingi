"""
Modèles de l'application blog.

- Category : classification des articles
- Post : article de blog
- PostImage : images associées à un article
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Catégorie permettant de classer les articles du blog."""

    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Nom",
        help_text="Nom unique de la catégorie.",
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Identifiant URL. Généré automatiquement à partir du nom s'il est vide.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description optionnelle de la catégorie.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créée le",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modifiée le",
    )

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Article de blog."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        PUBLISHED = "published", "Publié"

    title = models.CharField(
        max_length=255,
        verbose_name="Titre",
    )
    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Identifiant URL unique. Généré automatiquement à partir du titre s'il est vide.",
    )
    excerpt = models.TextField(
        verbose_name="Extrait",
        help_text="Résumé court affiché dans les listes d'articles.",
    )
    content = models.TextField(
        verbose_name="Contenu",
    )
    featured_image = models.ImageField(
        upload_to="blog/posts/featured/",
        verbose_name="Image à la une",
        help_text="Image principale de l'article.",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="blog_posts",
        verbose_name="Auteur",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Catégorie",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Statut",
        help_text="Brouillon ou publié.",
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mis en avant",
        help_text="Afficher cet article en position privilégiée.",
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Vues",
        help_text="Nombre de consultations de l'article.",
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Publié le",
        help_text="Date de publication. Renseignée automatiquement lors de la première publication.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Créé le",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modifié le",
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-published_at", "-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Renseigner published_at à la première publication
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)


class PostImage(models.Model):
    """Image associée à un article de blog."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Article",
    )
    image = models.ImageField(
        upload_to="blog/posts/gallery/",
        verbose_name="Image",
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Légende",
        help_text="Légende optionnelle de l'image.",
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordre",
        help_text="Position d'affichage (0 = première).",
    )

    class Meta:
        verbose_name = "Image d'article"
        verbose_name_plural = "Images d'article"
        ordering = ["order", "id"]

    def __str__(self) -> str:
        if self.caption:
            return f"{self.post.title} — {self.caption}"
        return f"{self.post.title} — image #{self.order}"
