Final peak


import streamlit as st
import os
import requests
import json
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# API Credentials
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Page Configuration
st.set_page_config(page_title="Multifunctional Legal Tool", layout="wide")
translator = Translator()

# Function to create a formatted complaint PDF
def create_pdf(text, filename):
    pdf_path = f"downloads/{filename}.pdf"
    os.makedirs("downloads", exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.drawString(100, 800, "Legal Complaint Document")
    y_position = 780
    for line in text.split("\n"):
        if y_position < 50:
            c.showPage()
            y_position = 800
        c.drawString(50, y_position, line)
        y_position -= 20
    c.save()
    return pdf_path

# Function to extract text from an image
def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang="hin+tam+eng").strip()

# Function to classify legal issues
def classify_legal_issue(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Classify the following legal issue into a complaint type: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "Error analyzing the issue.")

# Function to classify legal articles
def classify_article(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Find the most relevant constitutional articles for the following legal issue: {user_input}."
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "Error retrieving articles.")

# Function to generate formatted complaint text
def generate_complaint_text(name, address, issue, details):
    return f"""
To Whom It May Concern,

Subject: {issue} Complaint

Dear Sir/Madam,

I, {name}, residing at {address}, am writing to formally lodge a complaint regarding {issue}. Below are the details:

Details of Complaint:
{details}

I kindly request you to take appropriate action at the earliest.

Sincerely,
{name}
"""

# Streamlit App
st.title("\U0001F3DB️ Know Your Rights, Take Action")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚖️ Classify Issue & Articles", use_container_width=True):
        st.session_state.page = "classifier"

with col2:
    if st.button("\U0001F4E7 Email Drafting Assistant", use_container_width=True):
        st.session_state.page = "email_assistant"

with col3:
    if st.button("\U0001F5BC️ Image Extraction", use_container_width=True):
        st.session_state.page = "ocr"

if "page" in st.session_state:
    if st.session_state.page == "classifier":
        st.header("⚖️ Classify Legal Issue & Find Related Articles")
        user_input = st.text_area("Describe your legal issue:", height=150)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Classify Issue"):
                if user_input.strip():
                    classification_result = classify_legal_issue(user_input)
                    st.subheader("Classification Result:")
                    st.success(classification_result)
                else:
                    st.warning("Please enter a description before submitting.")
        
        with col2:
            if st.button("Classify Article"):
                if user_input.strip():
                    article_result = classify_article(user_input)
                    st.subheader("Relevant Constitutional Articles:")
                    st.info(article_result)
                else:
                    st.warning("Please enter a description before submitting.")
    
    elif st.session_state.page == "email_assistant":
        st.header("\U0001F4E7 Email Drafting Assistant")
        name = st.text_input("Your Name")
        address = st.text_area("Your Address")
        issue = st.text_input("Complaint Type (e.g., Consumer Complaint, RTI Request)")
        details = st.text_area("Describe Your Complaint/Request")
        
        if st.button("Generate Document"):
            if name and address and issue and details:
                complaint_text = generate_complaint_text(name, address, issue, details)
                pdf_path = create_pdf(complaint_text, "legal_complaint")
                st.success("Document generated successfully!")
                
                with open(pdf_path, "rb") as file:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button("Download PDF", file, file_name="legal_complaint.pdf", mime="application/pdf")
                    with col2:
                        st.markdown('<a href="https://mail.google.com" target="_blank" style="text-decoration:none;"><button style="background-color:#ff4b4b; color:white; padding:10px 15px; border:none; border-radius:5px; cursor:pointer;">\U0001F4E9 File a Complaint via Email</button></a>', unsafe_allow_html=True)
            else:
                st.error("Please fill in all fields.")
    
    elif st.session_state.page == "ocr":
        st.header("\U0001F5BC️ Text Extraction from Image")
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            extracted_text = extract_text_from_image(image)
            st.subheader("Extracted Text")
            st.write(extracted_text)
            translated_text = translator.translate(extracted_text, dest="en").text
            st.subheader("Translated Text (English)")
            st.write(translated_text)
