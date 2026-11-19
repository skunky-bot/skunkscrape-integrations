import json
import pytest
from skunky_integrations import prepare_webhook


def test_unverified_leads_blocked():
    with pytest.raises(PermissionError):
        prepare_webhook({
            "source_id": "fixture", "source_url": "https://example.com/",
            "consent_status": "unverified", "outreach_allowed": False,
        }, "https://crm.example.com/hook", "a" * 40)


def test_explicitly_approved_payload_signed():
    body, headers = prepare_webhook({
        "source_id": "fixture", "source_url": "https://example.com/",
        "consent_status": "verified", "outreach_allowed": True,
        "emails": ["contact@example.com"],
    }, "https://crm.example.com/hook", "a" * 40)
    assert json.loads(body)["emails"] == ["contact@example.com"]
    assert headers["X-Skunky-Signature"].startswith("sha256=")


def test_insecure_destinations_blocked():
    with pytest.raises(ValueError):
        prepare_webhook({"source_id": "fixture"}, "http://localhost:8080", "a" * 40)
