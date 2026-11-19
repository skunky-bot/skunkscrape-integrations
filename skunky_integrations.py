"""Pure outbound webhook preparation. Transport and credential management are separate."""
from __future__ import annotations

import hashlib
import hmac
import json
from urllib.parse import urlsplit


def prepare_webhook(lead: dict, endpoint: str, secret: str) -> tuple[bytes, dict]:
    """Prepare a signed payload only when explicit outreach/processing approval exists.

    This function DOES NOT transmit or persist the payload.
    """
    parts = urlsplit(endpoint)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        raise ValueError("Webhook destination must be credential-free HTTPS")
    if not secret or len(secret) < 16:
        raise ValueError("Strong signing secret required")
    if lead.get("outreach_allowed") is not True or lead.get("consent_status") != "verified":
        raise PermissionError("Contact export blocked pending verified authorization")
    if not lead.get("source_id") or not lead.get("source_url"):
        raise ValueError("Source provenance required")
    payload = {
        "source_id": lead["source_id"],
        "source_url": lead["source_url"],
        "emails": lead.get("emails", []),
        "phones": lead.get("phones", []),
        "consent_status": "verified",
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return body, {"Content-Type": "application/json", "X-Skunky-Signature": "sha256=" + digest}
