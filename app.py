import streamlit as st
import requests
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Load API Key from .env file
load_dotenv()
MISTRAL_API_KEY = os.getenv("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")

# Function to generate legal document using Mistral API
def generate_legal_text(prompt):
    url = "https://mistral.ai//generate"  # Replace with actual Mistral API URL
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "max_tokens": 500}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("text", "Error: No response from AI")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to create a PDF
def create_pdf(text, filename):
    pdf_path = f"downloads/{filename}.pdf"
    os.makedirs("downloads", exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, "Generated Legal Document")
    text_lines = text.split("\n")
    y_position = 780
    for line in text_lines:
        if y_position < 50:
            c.showPage()
            y_position = 800
        c.drawString(50, y_position, line)
        y_position -= 20
    c.save()
    return pdf_path

# Streamlit UI
st.title("Legal Document Generator")
st.write("Generate legal documents such as police complaints, RTI requests, consumer complaints, etc.")

# User input fields
document_type = st.selectbox("Select Document Type", ["Police Complaint", "RTI Request", "Consumer Complaint", "Legal Notice"])
name = st.text_input("Your Name")
address = st.text_area("Your Address")
details = st.text_area("Describe Your Complaint/Request")

if st.button("Generate Document"):
    if name and address and details:
        prompt = f"Generate a {document_type} for {name}, living at {address}. Details: {details}"
        generated_text = generate_legal_text(prompt)
        pdf_path = create_pdf(generated_text, "legal_document")
        st.success("Document generated successfully!")
        with open(pdf_path, "rb") as file:
            st.download_button("Download PDF", file, file_name="legal_document.pdf", mime="application/pdf")
    else:
        st.error("Please fill in all fields.")
