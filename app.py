import streamlit as st
import requests
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = "https://api.mistral.ai/v1/completions"

def classify_text(text, model="mistral-small-latest"):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    data = {"model": model, "prompt": text, "max_tokens": 50}
    response = requests.post(MISTRAL_API_URL, json=data, headers=headers)
    return response.json().get("choices")[0].get("text", "Error: No response")

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def translate_text(text, dest_lang='en'):
    translator = Translator()
    return translator.translate(text, dest=dest_lang).text

def generate_pdf(content, filename="legal_document.pdf"):
    pdf_path = os.path.join("./", filename)
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, content)
    c.save()
    return pdf_path

def send_complaint_email():
    st.success("Complaint filing via email functionality will be implemented here.")

st.title("🛡️ Legal Aid Assistant")

# Section 1: Legal Issue & Article Classification
st.header("📌 Classify Legal Issue & Article")
with st.container():
    text_input = st.text_area("Enter legal issue or article:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Classify Issue"):
            result = classify_text(text_input)
            st.write("Classification:", result)
    with col2:
        if st.button("Classify Article"):
            result = classify_text(text_input)
            st.write("Classification:", result)

# Section 2: Legal Document Generation
st.header("📄 Generate Legal Document")
with st.container():
    doc_text = st.text_area("Enter document content:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate PDF"):
            pdf_file = generate_pdf(doc_text)
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, file_name="legal_document.pdf", mime="application/pdf")
    with col2:
        if st.button("File a Complaint via Email"):
            send_complaint_email()

# Section 3: Image Text Extraction
st.header("🖼️ Extract Text from Image")
with st.container():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text_from_image(image)
        st.text_area("Extracted Text:", extracted_text, height=150)
        if st.button("Translate to English"):
            translated_text = translate_text(extracted_text)
            st.write("Translated Text:", translated_text)
