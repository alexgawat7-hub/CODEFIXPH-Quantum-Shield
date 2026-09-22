import streamlit as st
st.title("✅ CODEFIXPH Security Shield ACTIVE")
st.write("**Owner:** Alex Gawat Jr. | GENESIS-0001")
st.write("**Status:** READY TO USE - Production")
st.write("**Cert:** CFPH-QS-2026-0001")
st.divider()
ticket_id = st.selectbox("Ticket ID", ["1","2"])
user = st.text_input("User", "alex")
tickets = {"1":{"owner":"alex","content":"Ticket #1 SECURE"},"2":{"owner":"bob","content":"Ticket #2 PRIVATE"}}
if st.button("Check"):
    if tickets[ticket_id]["owner"] != user:
        st.error("403 FORBIDDEN - Shield Blocked")
    else:
        st.success(f"200 OK - {tickets[ticket_id]['content']}")
        st.balloons()
