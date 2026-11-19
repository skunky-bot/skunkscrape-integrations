# Skunky Integrations

Canonical location for outbound adapters (HubSpot, Salesforce, Dynamics, webhooks).

The initial `prepare_webhook` function **only prepares** a signed, minimal JSON payload. It does not transmit or persist anything and explicitly blocks unverified contacts and non-HTTPS destinations.

Production transport requires a separately reviewed worker: tenant-scoped OAuth, secret rotation, retries and DLQs, destination allowlisting, rate limits, idempotency, DNC/opt-outs, POPIA lawful basis and audit logging.

Do not treat `outreach_allowed` from untrusted callers as authoritative. Only trusted compliance services may issue export authorization. The initial implementation is a contract placeholder and not a ready-to-use CRM integration.
