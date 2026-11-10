import streamlit as st
from quantum_scanner import scan_website, ScanError
from datetime import datetime, timezone

st.set_page_config(
    page_title="Quantum Shield | CODEFIXPH",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CODEFIXPH — Quantum Shield
# Interactive educational demo. It does not protect external apps or real tickets.

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#eaf2ff;--muted:#9aaec8;--cyan:#55e0d0;--blue:#79aaff;--panel:#111c30;--line:#263955}
html,body,[class*="css"]{font-family:'Manrope',sans-serif}
.stApp{background:radial-gradient(ellipse at 8% 0%,#173451 0,transparent 34%),linear-gradient(160deg,#080e1b 0%,#0b1424 60%,#0a1020 100%);color:var(--ink)}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0c1729,#0a1220);border-right:1px solid #233550}
[data-testid="stSidebar"] *{color:#dce8f8}
.block-container{max-width:1320px;padding-top:2rem;padding-bottom:4rem}
.hero{padding:30px 32px;border:1px solid #2a405f;border-radius:24px;background:linear-gradient(120deg,#142943eF,#101b2eee);box-shadow:0 24px 70px #0005;margin:8px 0 20px}
.eyebrow{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.18em;color:#55e0d0;font-weight:500}
.hero h1{font-size:clamp(2rem,4vw,3.3rem);line-height:1.08;letter-spacing:-.05em;margin:.55rem 0;color:#f1f6ff}
.hero p{max-width:760px;color:#a9bad0;font-size:15px;margin:0}
.brandmark{display:inline-grid;place-items:center;width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,#55e0d0,#6d9dff);color:#071522;font-size:22px;font-weight:900;margin-right:10px}
.metric{background:linear-gradient(145deg,#14243b,#101a2b);border:1px solid #293e5d;border-radius:17px;padding:17px 18px;min-height:110px}
.metric-label{font:11px 'DM Mono',monospace;letter-spacing:.12em;color:#91a7c3;text-transform:uppercase}
.metric-value{font-size:25px;font-weight:800;color:#eaf3ff;margin-top:8px}
.metric-note{font-size:12px;color:#8fa5c1;margin-top:2px}
.panel{background:#111c30;border:1px solid #293d59;border-radius:18px;padding:20px 22px;margin:10px 0}
.panel h3{color:#edf5ff;font-size:18px;margin:0 0 6px}
.panel p{color:#9fb1c9}
.smallcaps{font:11px 'DM Mono',monospace;letter-spacing:.12em;color:#55e0d0}
.stButton>button{border-radius:11px;border:1px solid #3b5c78;background:linear-gradient(135deg,#55e0d0,#79aaff);color:#071522;font-weight:800;min-height:43px}
.stButton>button:hover{border-color:#8ef3e7;color:#06121e;filter:brightness(1.06)}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background:#0b1728;border-color:#344966;color:#eaf2ff;border-radius:10px}
.stTabs [data-baseweb="tab-list"]{gap:8px}
.stTabs [data-baseweb="tab"]{background:#101c2e;border:1px solid #263a56;border-radius:10px 10px 0 0;padding:10px 16px;color:#b9c9dd}
.stTabs [aria-selected="true"]{background:#183149!important;color:#63e6d7!important}
div[data-testid="stAlert"]{border-radius:12px}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

TICKETS = {
    "QS-1001": {"owner": "Alex", "title": "Profile access request", "classification": "Private"},
    "QS-1002": {"owner": "Bob", "title": "Account settings request", "classification": "Private"},
    "QS-1003": {"owner": "Alex", "title": "API key rotation request", "classification": "Restricted"},
    "QS-1004": {"owner": "Mia", "title": "Billing record request", "classification": "Confidential"},
}

if "identity" not in st.session_state:
    st.session_state.identity = "Alex"
if "events" not in st.session_state:
    st.session_state.events = []

with st.sidebar:
    st.markdown('<div class="eyebrow">CODEFIXPH / SECURITY LAB</div>', unsafe_allow_html=True)
    st.markdown("## 🛡️ Quantum Shield")
    st.caption("Genesis 0001 · Interactive security demo")
    st.divider()
    st.markdown("**Demo session identity**")
    selected = st.selectbox("Choose a test persona", ["Alex", "Bob", "Mia"], index=["Alex","Bob","Mia"].index(st.session_state.identity), label_visibility="collapsed")
    if selected != st.session_state.identity:
        st.session_state.identity = selected
        st.rerun()
    st.info("This selector simulates a signed-in identity for learning. It is not real account authentication.")
    st.divider()
    st.caption("CERTIFICATE REFERENCE")
    st.code("CFPH-QS-2026-0001", language=None)
    st.caption("Build · Interactive PoC")

st.markdown("""
<div class="hero">
  <div class="eyebrow"><span class="brandmark">Q</span> ACCESS CONTROL PLAYGROUND · GENESIS 0001</div>
  <h1>Quantum Shield</h1>
  <p>Explore how ownership checks can block Insecure Direct Object Reference (IDOR) attempts. Run safe tests against sample records and inspect each decision.</p>
</div>
""", unsafe_allow_html=True)

allowed_count = sum(1 for e in st.session_state.events if e["allowed"])
blocked_count = sum(1 for e in st.session_state.events if not e["allowed"])
cols = st.columns(4)
metrics = [
    ("DEMO STATUS", "ONLINE", "Interactive proof-of-concept"),
    ("SIGNED-IN PERSONA", st.session_state.identity.upper(), "Simulated test identity"),
    ("ACCESS GRANTED", str(allowed_count), "Successful sample checks"),
    ("ACCESS BLOCKED", str(blocked_count), "Ownership mismatches"),
]
for col, (label, value, note) in zip(cols, metrics):
    with col:
        st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

st.write("")
tab_test, tab_records, tab_audit, tab_scan, tab_about = st.tabs(["⚡ Access Lab", "▦ Sample Records", "◷ Test History", "⌕ Website Scan", "ⓘ About"])

with tab_test:
    st.markdown('<div class="smallcaps">01 / CONTROLLED IDOR TEST</div>', unsafe_allow_html=True)
    st.subheader("Run an access check")
    st.write(f"Current demo identity: **{st.session_state.identity}**. Choose a sample record to test its ownership boundary.")
    ticket_id = st.selectbox("Select sample record", list(TICKETS.keys()), format_func=lambda key: f"{key}  ·  {TICKETS[key]['title']}")
    ticket = TICKETS[ticket_id]
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown(f'<div class="panel"><div class="smallcaps">REQUEST PREVIEW</div><h3>{ticket_id}</h3><p>{ticket["title"]}</p><p>Record owner: <b>{ticket["owner"]}</b><br>Classification: <b>{ticket["classification"]}</b></p></div>', unsafe_allow_html=True)
        if st.button("Run ownership check", use_container_width=True, type="primary"):
            allowed = ticket["owner"] == st.session_state.identity
            event = {
                "time": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
                "identity": st.session_state.identity,
                "record": ticket_id,
                "owner": ticket["owner"],
                "allowed": allowed,
            }
            st.session_state.events.insert(0, event)
            st.session_state.last_result = event
            st.rerun()
    with right:
        st.markdown('<div class="panel"><div class="smallcaps">EXPECTED BEHAVIOR</div><h3>Owner match → allow</h3><p>Identity does not match owner → deny with 403.</p><p>Missing record → 404.</p></div>', unsafe_allow_html=True)
    if "last_result" in st.session_state:
        result = st.session_state.last_result
        if result["allowed"]:
            st.success(f"200 · ACCESS GRANTED — {result['identity']} owns {result['record']}.")
        else:
            st.error(f"403 · ACCESS DENIED — {result['identity']} does not own {result['record']}.")
        st.caption("This is a simulated authorization decision over local sample data, not a penetration test.")

with tab_records:
    st.markdown('<div class="smallcaps">02 / TEST DATASET</div>', unsafe_allow_html=True)
    st.subheader("Sample records")
    st.caption("Fictional records only. No real customer information is stored.")
    for key, item in TICKETS.items():
        with st.container(border=True):
            a, b, c = st.columns([1, 2, 1])
            a.markdown(f"**{key}**")
            b.write(item["title"])
            c.caption(f"{item['owner']} · {item['classification']}")

with tab_audit:
    st.markdown('<div class="smallcaps">03 / LOCAL TEST HISTORY</div>', unsafe_allow_html=True)
    st.subheader("Recent access decisions")
    if not st.session_state.events:
        st.info("No tests run in this session yet. Open Access Lab to run your first check.")
    else:
        for event in st.session_state.events[:20]:
            status = "ALLOWED" if event["allowed"] else "BLOCKED"
            st.write(f"**{status}** · {event['time']} · {event['identity']} → {event['record']} (owner: {event['owner']})")
    if st.button("Clear session history"):
        st.session_state.events = []
        st.session_state.pop("last_result", None)
        st.rerun()


with tab_scan:
    st.markdown('<div class="smallcaps">04 / PASSIVE WEBSITE SECURITY CHECK</div>', unsafe_allow_html=True)
    st.subheader("Check a website's basic security posture")
    st.caption("Only scan websites you own or have explicit permission to assess. This makes one bounded GET request and does not exploit or submit forms.")
    with st.form("quantum_website_scan"):
        target_url = st.text_input("Website URL", placeholder="https://example.com", max_chars=2048)
        submitted = st.form_submit_button("Run safe website check", type="primary")
    if submitted:
        try:
            st.session_state.website_report = scan_website(target_url)
        except ScanError as exc:
            st.error(str(exc))
    if "website_report" in st.session_state:
        report = st.session_state.website_report
        a, b, c = st.columns(3)
        a.metric("Posture score", f"{report['score']}/100")
        b.metric("Assessment", report["rating"])
        c.metric("HTTP status", report["http_status"])
        st.caption(f"Target: {report['target']}")
        st.download_button("Download JSON report", data=__import__("json").dumps(report, indent=2), file_name="quantum-shield-report.json", mime="application/json")
        for finding in report["findings"]:
            with st.container(border=True):
                st.markdown(f"**{finding['severity'].upper()} · {finding['title']}**")
                st.write(finding["detail"])
                st.info(f"Recommendation: {finding['recommendation']}")
        with st.expander("Scope and limitations"):
            for limitation in report["limitations"]:
                st.write(f"• {limitation}")
        st.warning("This is a limited HTTP header check, not a penetration test or security certification. A high score does not prove that a website is secure.")

with tab_about:
    st.markdown('<div class="smallcaps">04 / PROJECT INFORMATION</div>', unsafe_allow_html=True)
    st.subheader("CODEFIXPH — Quantum Shield")
    st.write("An educational security proof-of-concept demonstrating server-side ownership checks against IDOR-style access attempts.")
    st.markdown("""
    - **Project owner:** Alex Gawat Jr.
    - **Reference:** GENESIS-0001
    - **Certificate ID:** CFPH-QS-2026-0001
    - **Current scope:** local sample records and simulated identities
    - **Not included:** real authentication, external application scanning, production authorization middleware, independent security certification
    """)
    st.warning("This project is an educational demo, not a certified security product. Do not use it to protect real customer data without a proper authentication system, database-backed authorization, security review, and testing.")

st.divider()
st.caption("CODEFIXPH · QUANTUM SHIELD · CFPH-QS-2026-0001 · EDUCATIONAL SECURITY DEMO")
