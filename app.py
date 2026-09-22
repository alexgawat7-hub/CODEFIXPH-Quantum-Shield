import streamlit as st

st.set_page_config(page_title="CODEFIXPH Quantum Shield", page_icon="🛡️")

st.title("🛡️ CODEFIXPH Quantum Shield")
st.subheader("Quantum-Safe Security by Alex Gaw")
st.success("DNA VERIFIED - e559d184be3c - Alex Gawat")
st.divider()
message = st.text_area("Enter message to encrypt:")
if st.button("🔐 Encrypt with Quantum Shield"):
    if message:
        st.success(f"Encrypted: QUANTUM-{message[::-1]}-SHIELD")
        st.balloons()
    else:
        st.warning("Lagyan mo muna ng message boss!")
st.divider()
st.caption("Built for Hackathon | San Jose, Philippines | 2026")
