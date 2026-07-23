"""
Django production settings.
"""

import os

from .base import *  # noqa: F401, F403

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [
    'mapendomingi.org',
    '.up.railway.app',
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
