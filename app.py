import streamlit as st
import requests
import json
import os
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
MISTRAL_API_KEY = os.getenv("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

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

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang="hin+tam+eng").strip()

def classify_legal_issue(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Classify the following legal issue into a complaint type: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": prompt}]}
    
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "Error analyzing the issue.")

# Streamlit UI
st.set_page_config(page_title="Legal Assistant App", layout="wide")
st.title("📜 Legal Assistance Hub")

# Layout for 3 sections
col1, col2, col3 = st.columns(3)

# Card 1: Legal Issue Classifier & Article Generator
with col1:
    st.header("⚖️ Legal Issue Classifier")
    user_input = st.text_area("Describe your legal issue:", height=150)
    if st.button("Classify Issue"):
        if user_input.strip():
            classification_result = classify_legal_issue(user_input)
            st.subheader("Classification Result:")
            st.success(classification_result)
        else:
            st.warning("Please enter a description before submitting.")

# Card 2: Document Generator
with col2:
    st.header("📄 Legal Document Generator")
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
        else:
            st.error("Please fill in all fields.")

# Card 3: Image Text Extraction
with col3:
    st.header("🖼️ Text Extraction from Image")
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text_from_image(image)
        st.subheader("Extracted Text")
        st.write(extracted_text)
        translator = Translator()
        translated_text = translator.translate(extracted_text, dest="en").text
        st.subheader("Translated Text (English)")
        st.write(translated_text)
