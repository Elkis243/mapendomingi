"""Resolve Django settings module from DEBUG in .env."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


def get_settings_module() -> str:
    load_dotenv(BASE_DIR / '.env')
    if os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes'):
        return 'congif.settings.local'
    return 'congif.settings.production'
