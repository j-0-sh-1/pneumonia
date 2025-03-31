import streamlit as st

def open_gmail():
    gmail_url = "https://mail.google.com/"
    st.markdown(f"[Click here to open Gmail]({gmail_url})", unsafe_allow_html=True)

# Streamlit UI
st.title("Email Interface")
st.write("Click the button below to access Gmail.")

if st.button("Open Gmail"):
    open_gmail()
