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

st.title("Legal Complaint Filing App")

# Complaint Type Selection with Breakdown Button
selected_complaint = st.radio("Select Complaint Type", complaint_types)

# Navigation Button to visit Gmail
if st.button("File a Complaint via Gamil"):
    webbrowser.open_new_tab("https://mail.google.com")
