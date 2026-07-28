"""
Django production settings.
"""

import os

import dj_database_url

from .base import *  # noqa: F401, F403

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}

ALLOWED_HOSTS = [
    'mapendomingi-production.up.railway.app',
    'mapendomingi.org',
    'www.mapendomingi.org',
]

SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
)
SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'True') == 'True'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True') == 'True'

CSRF_TRUSTED_ORIGINS = [
    'https://*.up.railway.app',
    'https://mapendomingi.org',
    'https://www.mapendomingi.org',
]

X_FRAME_OPTIONS = os.getenv('X_FRAME_OPTIONS', 'DENY')
SECURE_BROWSER_XSS_FILTER = (
    os.getenv('SECURE_BROWSER_XSS_FILTER', 'True') == 'True'
)
SECURE_CONTENT_TYPE_NOSNIFF = (
    os.getenv('SECURE_CONTENT_TYPE_NOSNIFF', 'True') == 'True'
)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Médias : Cloudinary (local = filesystem via MEDIA_ROOT)
INSTALLED_APPS = [
    *INSTALLED_APPS,  # noqa: F405
    'cloudinary_storage',
    'cloudinary',
]

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUDINARY_CLOUD_NAME'],
    'API_KEY': os.environ['CLOUDINARY_API_KEY'],
    'API_SECRET': os.environ['CLOUDINARY_API_SECRET'],
}

STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Évite un crash si un fichier référencé manque au collectstatic
WHITENOISE_MANIFEST_STRICT = False
