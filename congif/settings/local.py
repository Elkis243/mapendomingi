"""
Django local development settings.
"""

import os

from .base import *  # noqa: F401, F403

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*']
