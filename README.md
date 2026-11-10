# CODEFIXPH — Quantum Shield

A lightweight security-learning project with two features:

1. **Access-control lab** — demonstrates server-side ownership checks against a small set of fictional records.
2. **Passive website security check** — checks a public website's HTTPS usage and selected HTTP security headers, then produces a JSON report.

## Live routes

- `/` — access-control demonstration.
- `/scan` — website security posture checker.
- `/scan/report.json` — download the most recent scan report from the current browser session.
- `/verify` — project metadata endpoint.
- `POST /api/v1/scan` — optional JSON API; requires a server-side `QUANTUM_API_KEY`.

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
export FLASK_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python app.py
```

Open `http://127.0.0.1:5000`.

For Render, use a Python web service with build command `pip install -r requirements.txt` and start command `gunicorn app:app`. Set a stable, random `FLASK_SECRET_KEY` in the service environment. To enable the JSON API, also set a long random `QUANTUM_API_KEY`. Never commit either secret to GitHub.

## API example

```bash
curl -X POST https://YOUR-HOST/api/v1/scan \
  -H "Authorization: Bearer YOUR_QUANTUM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Scan behavior and safety

- Only HTTP/HTTPS URLs are accepted.
- Localhost, private/reserved IPs, and domains resolving to non-public IPs are rejected.
- TLS certificate validation remains enabled.
- The scanner makes one bounded GET request with connect/read timeouts, does not follow redirects, does not submit forms, and does not attempt exploitation.
- The web form and API are rate-limited to 5 scans per hour per IP.
- The scan score is a simple heuristic based only on the checks listed in the report. It is not a probability, grade from an auditor, or guarantee.

**Only scan websites you own or have explicit permission to assess.**

## Important limitations

This is a first-pass HTTP configuration checker and educational proof-of-concept, not a full vulnerability scanner, penetration test, WAF, antivirus, compliance audit, or security certification. It does not inspect source code, dependencies, application logic, authentication flows, databases, or exploitability. A clean result does not mean a website is secure.

The access-control demonstration still uses fictional in-memory records and a simulated identity selector. Do not use that demo authentication or its sample records for real customer data.

## Deployment note

The repository's existing Render service configuration and live deployment have not been verified by this code change. Configure the Render service's build/start commands and environment variables as described above, then confirm the deployment health before sharing the live URL.
