import streamlit as st
import requests
import json
import os
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def classify_issue(user_input):
    MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
    MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        f"Classify the following legal issue into a complaint type: {user_input}\n"
        "Options: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
    )
    
    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    return "Error analyzing the issue. Please try again."

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang="hin+tam+eng").strip()

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

# UI DESIGN
st.set_page_config(page_title="Legal Issue Analyzer", layout="wide")
st.title("⚖️ Legal Issue Analyzer & Tools")
st.write("Use the tools below to analyze legal issues, extract text, and generate legal documents.")

# Three Cards Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
            <h3>🔍 Classify Legal Issue</h3>
            <p>Classify your legal issue into the appropriate category.</p>
            <a href='#classify'><button style='padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 5px;'>Go</button></a>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
            <h3>🖼️ Extract Text from Image</h3>
            <p>Upload an image and extract text for legal purposes.</p>
            <a href='#ocr'><button style='padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px;'>Go</button></a>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
            <h3>📄 Generate Legal Document</h3>
            <p>Generate a legal document from your complaint details.</p>
            <a href='#document'><button style='padding: 10px; background-color: #dc3545; color: white; border: none; border-radius: 5px;'>Go</button></a>
        </div>
    """, unsafe_allow_html=True)

# Classify Section
st.subheader("🔍 Classify Legal Issue", anchor="classify")
user_input = st.text_area("Describe your legal issue:", height=100)
if st.button("Classify Issue"):
    if user_input.strip():
        result = classify_issue(user_input)
        st.success(f"Classification: {result}")
    else:
        st.warning("Please enter a description.")

# OCR Section
st.subheader("🖼️ Extract Text from Image", anchor="ocr")
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
translator = Translator()
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    extracted_text = extract_text_from_image(image)
    st.subheader("Extracted Text")
    st.write(extracted_text)
    translated_text = translator.translate(extracted_text, dest="en").text
    st.subheader("Translated Text (English)")
    st.write(translated_text)

# Document Generator
st.subheader("📄 Generate Legal Document", anchor="document")
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
