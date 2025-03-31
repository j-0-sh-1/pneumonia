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

# Streamlit App
st.title("\U0001F5BC️ Text Extraction and Translation")

# File Uploader
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Language Selection
language = st.selectbox("Select language", ["Hindi", "Tamil", "English", "Bengali", "Telugu", "Gujarati", "Malayalam"])

# Language Mapping for OCR
language_mapping = {
    "Hindi": "hin",
    "Tamil": "tam",
    "English": "eng",
    "Bengali": "ben",
    "Telugu": "tel",
    "Gujarati": "guj",
    "Malayalam": "mal"
}

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Extract Text
    selected_language = language_mapping.get(language, "eng")
    extracted_text = pytesseract.image_to_string(image, lang=selected_language).strip()
    st.subheader("Extracted Text")
    st.write(extracted_text)
    
    # Translate Text
    translated_text = translator.translate(extracted_text, src=selected_language, dest="en").text
    st.subheader(f"Translated Text (English) from {language}")
    st.write(translated_text)
