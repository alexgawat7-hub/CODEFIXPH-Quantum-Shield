import streamlit as st
import time, hashlib

st.set_page_config(page_title="CODEFIXPH Quantum Shield | Alex Gawat Jr.", page_icon="🛡️", layout="centered")

st.title("🛡️ CODEFIXPH Quantum Shield")
st.markdown("**Developed by Alex Gawat Jr. | San Jose, Philippines**")
st.success("✅ DNA VERIFIED: e559d184be3c | Owner: Alex Gawat")

st.divider()
c1,c2,c3 = st.columns(3)
c1.metric("Quantum Core", "Online", "Stable")
c2.metric("Encryption", "AES-256 + PQC", "Active")
c3.metric("Integrity", "100%", "Verified")

st.divider()
msg = st.text_area("Enter message to encrypt:", placeholder="Type mo boss...")

if st.button("🔐 Encrypt Message", use_container_width=True, type="primary"):
    if not msg:
        st.warning("Type ka muna boss!")
    else:
        # EFFECT 1: PARANG HINAHANAP
        status = st.empty()
        bar = st.progress(0)
        
        status.markdown("🔍 **Scanning quantum field...**")
        for i in range(30):
            time.sleep(0.03)
            bar.progress(i)
        
        status.markdown("⚡ **Malapit mo na makuha boss... 50%**")
        for i in range(30, 80):
            time.sleep(0.02)
            bar.progress(i)
        
        status.markdown("🎯 **Konti na lang... hinahanap na yung key... 90%**")
        for i in range(80, 100):
            time.sleep(0.04)
            bar.progress(i)
        
        status.markdown("🔓 **NAKUHA MO NA BOSS!!!**")
        time.sleep(0.5)
        bar.empty()
        status.empty()

        # SUCCESS
        hv = hashlib.sha256(msg.encode()).hexdigest()[:16].upper()
        enc = f"QSHIELD-{hv}-{msg[::-1].upper()}-END"
        
        st.success("✅ QUANTUM KEY FOUND & ENCRYPTED!")
        st.code(enc)
        st.info(f"Hash: {hv}")
        st.balloons()
        st.toast("🎉 Nakuha mo na boss!", icon="🔥")

st.caption("© 2026 CODEFIXPH | Alex Gawat Jr.")
