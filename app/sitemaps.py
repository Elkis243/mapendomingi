"""Sitemaps dynamiques : pages vitrine + articles publiés."""

import os
from urllib.parse import urlparse

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


def _sitemap_domain():
    origin = os.getenv("SEO_ORIGIN", "").rstrip("/")
    if origin:
        return urlparse(origin).netloc
    return None


class StaticViewSitemap(Sitemap):
    """Pages statiques du site."""

    protocol = "https"
    changefreq = "monthly"
    priority = 0.8

    def get_domain(self, site=None):
        return _sitemap_domain() or super().get_domain(site)

    def items(self):
        return [
            ("app:home", 1.0, "weekly"),
            ("app:about", 0.8, "monthly"),
            ("app:donate", 0.9, "monthly"),
            ("app:contact", 0.7, "monthly"),
            ("blog:post_list", 0.7, "weekly"),
            ("app:domain_detail", 0.8, "monthly", {"slug": "femme-enfant"}),
            ("app:domain_detail", 0.8, "monthly", {"slug": "education-jeunesse"}),
            ("app:domain_detail", 0.8, "monthly", {"slug": "sante-durable"}),
        ]

    def location(self, item):
        name, _priority, _changefreq, *rest = item
        kwargs = rest[0] if rest else {}
        return reverse(name, kwargs=kwargs)

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class PostSitemap(Sitemap):
    """Articles de blog publiés — mis à jour automatiquement."""

    protocol = "https"
    changefreq = "monthly"
    priority = 0.6

    def get_domain(self, site=None):
        return _sitemap_domain() or super().get_domain(site)

    def items(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .order_by("-published_at", "-created_at")
        )

    def lastmod(self, obj):
        return obj.updated_at or obj.published_at

    def location(self, obj):
        return reverse("blog:post_detail", kwargs={"slug": obj.slug})
