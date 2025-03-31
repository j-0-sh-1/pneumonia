import streamlit as st
import requests
import json
import os
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- CONFIG ---
st.set_page_config(page_title="Legal Assistant Tool", layout="wide")
translator = Translator()

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "YOUR_API_KEY"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- FUNCTIONS ---
def classify_issue(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": f"Classify this legal issue: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment."}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: Unable to classify.")

def find_legal_sections(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": f"Find legal sections under Indian law for: {user_input}"}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: Unable to retrieve sections.")

def create_pdf(text, filename):
    pdf_path = f"downloads/{filename}.pdf"
    os.makedirs("downloads", exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, "Generated Legal Document")
    y_position = 780
    for line in text.split("\n"):
        if y_position < 50:
            c.showPage()
            y_position = 800
        c.drawString(50, y_position, line)
        y_position -= 20
    c.save()
    return pdf_path

# --- UI ---
st.title("⚖️ Legal Assistant Tool")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Classify Legal Issue", use_container_width=True):
        st.session_state.page = "classify"

with col2:
    if st.button("📜 Find Legal Sections", use_container_width=True):
        st.session_state.page = "sections"

with col3:
    if st.button("📝 Generate Legal Document", use_container_width=True):
        st.session_state.page = "document"

if "page" in st.session_state:
    if st.session_state.page == "classify":
        st.header("🔍 Legal Issue Classification")
        user_input = st.text_area("Describe your legal issue:", height=150)
        if st.button("Classify"):
            if user_input.strip():
                result = classify_issue(user_input)
                st.success(result)
            else:
                st.warning("Please enter a description.")
    
    elif st.session_state.page == "sections":
        st.header("📜 Relevant Legal Provisions")
        user_input = st.text_area("Describe your legal issue:", height=150)
        if st.button("Find Sections"):
            if user_input.strip():
                result = find_legal_sections(user_input)
                st.info(result)
            else:
                st.warning("Please enter a description.")

    elif st.session_state.page == "document":
        st.header("📝 Legal Document Generator")
        name = st.text_input("Your Name")
        address = st.text_area("Your Address")
        details = st.text_area("Describe Your Complaint/Request")
        if st.button("Generate Document"):
            if name and address and details:
                generated_text = f"Legal Document for {name} at {address}\nDetails: {details}"
                pdf_path = create_pdf(generated_text, "legal_document")
                st.success("Document generated successfully!")
                with open(pdf_path, "rb") as file:
                    st.download_button("Download PDF", file, file_name="legal_document.pdf", mime="application/pdf")
                    st.markdown("[📩 File a Complaint via Gmail](https://mail.google.com)", unsafe_allow_html=True)
            else:
                st.error("Please fill in all fields.")
