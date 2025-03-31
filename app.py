import streamlit as st

# Streamlit UI for Email Input
st.title("📧 Complaint Email Interface")

with st.form("email_form"):
    sender_email = st.text_input("From", "your-email@gmail.com")
    recipient_email = st.text_input("To", "recipient@gmail.com")
    subject = st.text_input("Subject", "Complaint Regarding...")
    body = st.text_area("Description", "Enter complaint details here...")
    
    send_email = st.form_submit_button("Send Email")

if send_email:
    st.success(f"Email to {recipient_email} has been drafted successfully!")
