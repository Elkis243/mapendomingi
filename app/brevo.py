"""Envoi d'emails transactionnels via l'API Brevo v3."""

from __future__ import annotations

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BREVO_SMTP_EMAIL_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoError(Exception):
    """Échec d'envoi via l'API Brevo."""


def send_transactional_email(
    *,
    to_email: str,
    subject: str,
    text_content: str,
    reply_to_email: str | None = None,
    reply_to_name: str | None = None,
    sender_email: str | None = None,
    sender_name: str = "MAPENDO MINGI",
) -> None:
    api_key = getattr(settings, "BREVO_API_KEY", "") or ""
    if not api_key:
        raise BrevoError("BREVO_API_KEY n'est pas configurée.")

    from_email = sender_email or settings.DEFAULT_FROM_EMAIL
    if not from_email:
        raise BrevoError("DEFAULT_FROM_EMAIL n'est pas configurée.")

    payload: dict = {
        "sender": {"name": sender_name, "email": from_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": text_content,
    }
    if reply_to_email:
        reply_to: dict = {"email": reply_to_email}
        if reply_to_name:
            reply_to["name"] = reply_to_name
        payload["replyTo"] = reply_to

    try:
        response = requests.post(
            BREVO_SMTP_EMAIL_URL,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": api_key,
            },
            json=payload,
            timeout=getattr(settings, "EMAIL_TIMEOUT", 15),
        )
    except requests.RequestException as exc:
        logger.exception("Erreur réseau Brevo")
        raise BrevoError("Impossible de contacter le service d'envoi d'emails.") from exc

    if response.status_code >= 400:
        logger.error(
            "Échec Brevo HTTP %s: %s",
            response.status_code,
            response.text[:500],
        )
        raise BrevoError("L'envoi de l'email a échoué.")
