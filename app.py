import os
import secrets
from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("RENDER") == "true",
)

# Deliberately small, in-memory sample data for the Quantum Shield demo.
# This is a teaching/demo environment, not a production ticket service.
TICKETS = {
    "1": {"owner": "alex", "content": "Ticket #1 — Alex's private sample record"},
    "2": {"owner": "bob", "content": "Ticket #2 — Bob's private sample record"},
}
DEMO_USERS = {"alex": "Alex", "bob": "Bob"}

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CODEFIXPH · Quantum Shield</title>
<style>
:root{color-scheme:dark;--bg:#080d19;--panel:#111a2b;--line:#26354d;--muted:#91a3bb;--text:#eef5ff;--cyan:#56e0d0;--blue:#70a7ff;--red:#ff7385}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 12% 0%,#15304a 0,transparent 38%),var(--bg);color:var(--text);font:15px/1.6 Inter,system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1050px;margin:auto;padding:32px 20px 60px}.top{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px}.mark{width:44px;height:44px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,#56e0d0,#4388ff);color:#061321;font-size:23px;font-weight:900;box-shadow:0 8px 30px #56e0d033}
.eyebrow{font-size:11px;letter-spacing:.18em;color:var(--cyan);font-weight:800}.brand h1{margin:0;font-size:20px;letter-spacing:.02em}.pill{border:1px solid #4c657f;border-radius:999px;padding:6px 11px;color:#c4d5e9;font-size:12px}
.hero{margin:34px 0 22px;padding:30px;border:1px solid var(--line);border-radius:24px;background:linear-gradient(120deg,#14243aee,#101827ee);box-shadow:0 24px 70px #0005}
.hero h2{font-size:clamp(28px,5vw,42px);line-height:1.08;margin:10px 0}.hero p{color:var(--muted);max-width:680px;margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:16px 0}.card{background:#111a2b;border:1px solid var(--line);border-radius:18px;padding:19px}.label{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em}.value{font-size:24px;font-weight:800;margin-top:7px}.good{color:var(--cyan)}.blue{color:var(--blue)}
section{margin-top:18px}.card h3{margin:0 0 8px}.card p{margin:0;color:var(--muted)}
select,button{font:inherit;border-radius:10px;padding:11px 13px;border:1px solid #354963;background:#0b1423;color:var(--text)}button{cursor:pointer;background:linear-gradient(135deg,#56e0d0,#6aa4ff);color:#071421;border:0;font-weight:800}button:hover{filter:brightness(1.08)}
form{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:12px}.notice{border:1px solid #765d2f;background:#2b2416;color:#f4d69b;padding:13px 16px;border-radius:13px;margin-top:16px;font-size:13px}
.result{padding:14px;border-radius:12px;margin-top:14px;background:#102b2a;border:1px solid #23635d}.denied{background:#301a24;border-color:#7a3349}.muted{color:var(--muted);font-size:13px}a{color:var(--cyan)}
footer{margin-top:30px;color:#71839c;font-size:12px;border-top:1px solid var(--line);padding-top:16px}
@media(max-width:600px){main{padding:20px 14px 40px}.hero{padding:22px}.top{align-items:flex-start}}
</style></head>
<body><main>
<header class="top"><div class="brand"><div class="mark">Q</div><div><div class="eyebrow">CODEFIXPH / SECURITY LAB</div><h1>QUANTUM SHIELD</h1></div></div><span class="pill">INTERACTIVE DEMO · GENESIS 0001</span></header>
<div class="hero"><div class="eyebrow">ACCESS CONTROL PLAYGROUND</div><h2>Test access boundaries.<br><span style="color:var(--cyan)">See the shield respond.</span></h2><p>Explore a controlled IDOR (Insecure Direct Object Reference) example. The server checks the identity stored in your signed session—not a username supplied in the ticket URL.</p></div>
<div class="grid"><div class="card"><div class="label">Demo status</div><div class="value good">ONLINE</div><p>Interactive security lab</p></div><div class="card"><div class="label">Protection example</div><div class="value blue">IDOR</div><p>Server-side ownership check</p></div><div class="card"><div class="label">Certificate ID</div><div class="value">CFPH-QS-2026-0001</div><p>Project reference</p></div></div>
<section class="card"><h3>01 / Choose demo identity</h3><p class="muted">This selector simulates a signed-in test persona. It is for demonstration only, not real account authentication.</p>
<form method="post" action="/demo/login"><select name="identity"><option value="alex" {{'selected' if identity == 'alex' else ''}}>Alex — Ticket 1 owner</option><option value="bob" {{'selected' if identity == 'bob' else ''}}>Bob — Ticket 2 owner</option></select><button type="submit">Set demo identity</button></form>
{% if identity %}<p class="muted" style="margin-top:12px">Current session identity: <strong>{{ display_name }}</strong></p>{% else %}<p class="muted" style="margin-top:12px">No identity selected. Set a demo identity to run the access test.</p>{% endif %}</section>
<section class="card"><h3>02 / Run an access-control test</h3><p class="muted">Select a sample record. The server uses your session identity to decide whether access is allowed.</p>
<div class="grid"><div><form method="post" action="/ticket/1"><button type="submit">Test Ticket #1 · Alex</button></form></div><div><form method="post" action="/ticket/2"><button type="submit">Test Ticket #2 · Bob</button></form></div></div>
{% if result %}<div class="result {{'denied' if not allowed else ''}}"><strong>{{ result }}</strong><div class="muted">{{ detail }}</div></div>{% endif %}</section>
<div class="notice"><strong>Scope note:</strong> Quantum Shield is currently an educational proof-of-concept. It is not a certified security product and has not undergone an independent penetration test. Demo records are stored in memory and reset when the service restarts.</div>
<footer>CODEFIXPH · Quantum Shield · {{ cert }} · Built for safe security learning</footer>
</main></body></html>
"""

@app.get("/")
def home():
    identity = session.get("demo_identity")
    result = session.pop("test_result", None)
    return render_template_string(
        PAGE,
        identity=identity,
        display_name=DEMO_USERS.get(identity, ""),
        result=result.get("message") if result else None,
        detail=result.get("detail") if result else None,
        allowed=result.get("allowed", False) if result else False,
        cert="CFPH-QS-2026-0001",
    )

@app.post("/demo/login")
def set_demo_identity():
    identity = request.form.get("identity", "")
    if identity in DEMO_USERS:
        session["demo_identity"] = identity
    return redirect(url_for("home"))

@app.post("/ticket/<ticket_id>")
def get_ticket(ticket_id):
    identity = session.get("demo_identity")
    if not identity:
        session["test_result"] = {
            "allowed": False,
            "message": "401 · DEMO IDENTITY REQUIRED",
            "detail": "Choose a demo identity before testing access.",
        }
        return redirect(url_for("home"))

    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        session["test_result"] = {
            "allowed": False,
            "message": "404 · RECORD NOT FOUND",
            "detail": "The requested sample record does not exist.",
        }
    elif ticket["owner"] != identity:
        session["test_result"] = {
            "allowed": False,
            "message": "403 · ACCESS DENIED",
            "detail": "The signed session identity does not own this sample record. The server blocked the request.",
        }
    else:
        session["test_result"] = {
            "allowed": True,
            "message": "200 · ACCESS GRANTED",
            "detail": ticket["content"],
        }
    return redirect(url_for("home"))

@app.get("/verify")
def verify():
    return jsonify({
        "owner": "Alex Gawat Jr.",
        "project": "CODEFIXPH-Quantum-Shield",
        "certificate": "CFPH-QS-2026-0001",
        "status": "Educational proof-of-concept",
        "security_demo": "Session-based ownership check for sample tickets",
        "production_certification": False,
    })


# Quantum Shield passive website scanner
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from quantum_scanner import scan_website, ScanError
import json
from functools import wraps

limiter = Limiter(get_remote_address, app=app, default_limits=["120 per hour"], storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"))

SCAN_PAGE = """
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quantum Shield · Website Check</title><style>
:root{color-scheme:dark;--bg:#080d19;--panel:#111a2b;--line:#26354d;--muted:#91a3bb;--text:#eef5ff;--cyan:#56e0d0;--red:#ff7385}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 12% 0%,#15304a 0,transparent 38%),var(--bg);color:var(--text);font:15px/1.6 system-ui,sans-serif}
main{max-width:980px;margin:auto;padding:28px 18px 60px}.top{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}.brand{font-weight:900;letter-spacing:.08em}.brand span{color:var(--cyan)}a{color:var(--cyan)}
.hero,.card{border:1px solid var(--line);background:linear-gradient(140deg,#14243a,#101827);border-radius:20px;padding:22px;margin-top:18px}.eyebrow{color:var(--cyan);font-size:11px;letter-spacing:.16em;font-weight:800}.hero h1{font-size:clamp(28px,5vw,42px);line-height:1.1;margin:8px 0}.muted{color:var(--muted);font-size:13px}
form{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}input{flex:1;min-width:220px;background:#081321;border:1px solid #344966;border-radius:10px;padding:13px;color:var(--text);font:inherit}button,.download{border:0;border-radius:10px;background:linear-gradient(135deg,#56e0d0,#70a7ff);padding:12px 18px;color:#071421;font-weight:900;font:inherit;text-decoration:none;cursor:pointer}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}.stat{background:#0c1728;border:1px solid var(--line);border-radius:14px;padding:15px}.num{font-size:28px;font-weight:900}.finding{border:1px solid var(--line);border-radius:14px;padding:15px;margin:10px 0;background:#0d1727}.sev{font-size:11px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.high,.critical{color:#ff8291}.medium{color:#ffc66e}.low{color:#8cb8ff}.info{color:var(--cyan)}.error{background:#301a24;border:1px solid #7a3349;padding:12px;border-radius:12px;margin-top:15px}
@media(max-width:600px){main{padding:18px 13px}.hero,.card{padding:18px}form button{width:100%}}
</style></head><body><main>
<div class="top"><div class="brand">CODEFIXPH <span> / QUANTUM SHIELD</span></div><a href="/">Access-control demo</a></div>
<div class="hero"><div class="eyebrow">PASSIVE WEBSITE SECURITY CHECK</div><h1>See your website's security posture.</h1><p class="muted">Checks basic HTTPS and response security headers. One bounded request, no exploit attempts, no form submissions, and redirects are not followed.</p>
<form method="post" action="/scan"><input name="url" type="url" placeholder="https://example.com" value="{{ target }}" required maxlength="2048"><button type="submit">Run safe check</button></form>
<p class="muted">Only scan websites you own or have explicit permission to assess. Public website checks are limited to 5 per hour per IP.</p></div>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
{% if report %}<section class="card"><div class="eyebrow">SCAN SUMMARY</div><div class="stats">
<div class="stat"><div class="muted">POSTURE SCORE</div><div class="num">{{ report.score }}/100</div></div>
<div class="stat"><div class="muted">ASSESSMENT</div><div class="num" style="font-size:20px">{{ report.rating }}</div></div>
<div class="stat"><div class="muted">HTTP STATUS</div><div class="num">{{ report.http_status }}</div></div>
<div class="stat"><div class="muted">FINDINGS</div><div class="num">{{ report.findings|length }}</div></div></div>
<p class="muted">Target: {{ report.target }}</p><a class="download" href="/scan/report.json">Download JSON report</a></section>
<section class="card"><div class="eyebrow">DETAILED FINDINGS</div><h2>What Quantum Shield observed</h2>
{% for item in report.findings %}<div class="finding"><div class="sev {{ item.severity }}">{{ item.severity }}</div><strong>{{ item.title }}</strong><p class="muted">{{ item.detail }}</p><p><strong>Recommendation:</strong> {{ item.recommendation }}</p></div>{% endfor %}</section>
<section class="card"><div class="eyebrow">SCOPE & LIMITATIONS</div><ul>{% for item in report.limitations %}<li class="muted">{{ item }}</li>{% endfor %}</ul></section>{% endif %}
<section class="card"><div class="eyebrow">PRODUCT SCOPE</div><p class="muted">Quantum Shield is a lightweight first-pass HTTP configuration checker and an educational access-control lab. It is not a vulnerability scanner, penetration test, compliance audit, or security certification.</p></section>
</main></body></html>
"""

@app.get("/scan")
def scan_home():
    return render_template_string(SCAN_PAGE, report=session.get("last_scan"), target="", error=None)

@app.post("/scan")
@limiter.limit("5 per hour")
def scan_submit():
    target = request.form.get("url", "")
    try:
        report = scan_website(target)
        session["last_scan"] = report
        return render_template_string(SCAN_PAGE, report=report, target=target, error=None)
    except ScanError as exc:
        return render_template_string(SCAN_PAGE, report=None, target=target, error=str(exc)), 400

@app.get("/scan/report.json")
def scan_report_download():
    report = session.get("last_scan")
    if not report:
        return jsonify({"error": "Run a website check before downloading a report."}), 404
    response = app.response_class(json.dumps(report, indent=2), mimetype="application/json")
    response.headers["Content-Disposition"] = "attachment; filename=quantum-shield-report.json"
    return response

@app.post("/api/v1/scan")
@limiter.limit("5 per hour")
def scan_api():
    expected_key = os.environ.get("QUANTUM_API_KEY")
    supplied = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    if not expected_key or not secrets.compare_digest(supplied, expected_key):
        return jsonify({"error": "API access is disabled or the bearer token is invalid. Configure QUANTUM_API_KEY on the server."}), 401
    payload = request.get_json(silent=True) or {}
    try:
        report = scan_website(payload.get("url", ""))
        return jsonify(report)
    except ScanError as exc:
        return jsonify({"error": str(exc)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
