"""Résout le module de settings Django depuis .env.

- Local (DJANGO_DEBUG=True)  → congif.settings.local
- Production (DJANGO_DEBUG=False) → DJANGO_SETTINGS_MODULE (.env)
  ou congif.settings.production par défaut
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

LOCAL_SETTINGS = 'congif.settings.local'
PRODUCTION_SETTINGS = 'congif.settings.production'


def get_settings_module() -> str:
    load_dotenv(BASE_DIR / '.env')

    debug = os.getenv('DJANGO_DEBUG', os.getenv('DEBUG', 'False'))
    if debug.lower() in ('true', '1', 'yes'):
        return LOCAL_SETTINGS

    return os.getenv('DJANGO_SETTINGS_MODULE', PRODUCTION_SETTINGS)
