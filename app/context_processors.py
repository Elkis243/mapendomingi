"""Context processor SEO : origin, canonical, sitemap."""

import os


def seo(request):
    configured_origin = os.getenv("SEO_ORIGIN", "").rstrip("/")
    if configured_origin:
        origin = configured_origin
    else:
        origin = f"{request.scheme}://{request.get_host()}".rstrip("/")

    path = request.path
    canonical = f"{origin}{path}"
    if path != "/" and canonical.endswith("/"):
        # conserver le slash final tel que servi
        pass

    # Retirer query string éventuelle
    canonical = canonical.split("?", 1)[0]

    return {
        "SEO_LANG": "fr",
        "SEO_LOCALE": "fr_CD",
        "SEO_ORIGIN": origin,
        "SEO_CANONICAL_URL": canonical,
        "SEO_SITEMAP_URL": f"{origin}/sitemap.xml",
    }
