import streamlit as st
import webbrowser

# List of complaint types
complaint_types = [
    "Consumer Complaint",
    "Criminal Complaint",
    "Civil Complaint",
    "Workplace Harassment",
    "Legal Notice",
    "Government Complaint",
    "Cybercrime Report",
    "Intellectual Property Violation",
    "Tenant-Landlord Dispute",
    "Environmental Complaint"
]

def generate_email_body(complaint_type):
    return f"""
    Dear [Recipient],
    
    I would like to file a {complaint_type} regarding [mention issue briefly].
    
    Details:
    - Name: [Your Name]
    - Contact: [Your Contact Information]
    - Description: [Provide full details of the complaint]
    
    Kindly address this issue at the earliest.
    
    Best Regards,
    [Your Name]
    """

st.title("Legal Complaint Filing App")

# Complaint Type Selection
selected_complaint = st.selectbox("Select Complaint Type", complaint_types)

def open_gmail():
    email_body = generate_email_body(selected_complaint)
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={selected_complaint} Complaint&body={email_body}"
    webbrowser.open(gmail_url)

# Button to open Gmail
if st.button("File Complaint via Gmail"):
    open_gmail()
