import streamlit as st
import webbrowser
from fpdf import FPDF

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
if st.button("Go to Gmail"):
    webbrowser.open_new_tab("https://mail.google.com")

# Function to generate a PDF with an image
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Complaint Details", ln=True, align='C')
    pdf.image("sample_image.jpg", x=10, y=30, w=100)  # Replace with actual image path
    pdf_output = "complaint.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Button to download PDF
if st.button("Download Complaint PDF"):
    pdf_file = generate_pdf()
    with open(pdf_file, "rb") as file:
        st.download_button(label="Download PDF", data=file, file_name="complaint.pdf", mime="application/pdf")
