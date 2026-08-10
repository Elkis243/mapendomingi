"""Helpers SEO — images de partage Open Graph 1200×630."""

from __future__ import annotations

OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_IMAGE_TYPE_WEBP = "image/webp"
OG_IMAGE_TYPE_JPEG = "image/jpeg"

_CLOUDINARY_UPLOAD = "/image/upload/"
_OG_TRANSFORM = "c_fill,w_1200,h_630,f_jpg,q_auto"


def cloudinary_share_url(url: str) -> str | None:
    """Insère une transformation 1200×630 JPG sur une URL Cloudinary."""
    if not url or "res.cloudinary.com" not in url or _CLOUDINARY_UPLOAD not in url:
        return None
    prefix, rest = url.split(_CLOUDINARY_UPLOAD, 1)
    if rest.startswith(f"{_OG_TRANSFORM}/"):
        return url
    return f"{prefix}{_CLOUDINARY_UPLOAD}{_OG_TRANSFORM}/{rest}"


def blog_share_image(
    *,
    featured_url: str | None,
    fallback_url: str,
) -> dict[str, str | int]:
    """
    Retourne url / type / width / height pour les metas OG/Twitter d'un article.

    - Cloudinary : crop fill 1200×630 en JPG
    - Sinon : image sociale par défaut (déjà 1200×630)
    """
    if featured_url:
        transformed = cloudinary_share_url(featured_url)
        if transformed:
            return {
                "url": transformed,
                "type": OG_IMAGE_TYPE_JPEG,
                "width": OG_IMAGE_WIDTH,
                "height": OG_IMAGE_HEIGHT,
            }

    return {
        "url": fallback_url,
        "type": OG_IMAGE_TYPE_WEBP,
        "width": OG_IMAGE_WIDTH,
        "height": OG_IMAGE_HEIGHT,
    }
