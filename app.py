import streamlit as st
import requests
import os
import pytesseract
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from googletrans import Translator
from PIL import Image

# Load API Key from .env file
load_dotenv()
MISTRAL_API_KEY = os.getenv("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")  # Set API key in .env

# Set Tesseract OCR Path (For Windows, change accordingly)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Modify this path if needed

# Initialize translator
translator = Translator()

# ---- FUNCTION TO GENERATE TEXT USING AI ----
def generate_legal_text(prompt):
    url = "https://api.mistral.ai/v1/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-7b",  # Adjust model if needed
        "prompt": prompt,
        "max_tokens": 500
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "Error: No text returned.")
    else:
        return "Error: API request failed."

# ---- FUNCTION TO CREATE PDF ----
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

# ---- FUNCTION TO EXTRACT TEXT FROM IMAGE ----
def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image, lang="hin+tam+eng")  # Extract Hindi, Tamil, and English
    return extracted_text.strip()

# ---- FUNCTION TO TRANSLATE TEXT ----
def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"

# ---- FUNCTION TO SUMMARIZE TEXT ---- (Simple Extractive Summarization)
def summarize_text(text):
    sentences = text.split(". ")
    if len(sentences) > 3:
        return ". ".join(sentences[:3]) + "..."
    return text  # Return as is if text is short

# ---- STREAMLIT UI ----
st.title("Multilingual Legal Document & OCR Interface")
st.write("Generate legal documents, extract text from images, translate, and summarize.")

# ---- MULTILINGUAL SELECTION ----
language = st.selectbox("Select Language", ["English", "Hindi", "Tamil"])
lang_map = {"English": "en", "Hindi": "hi", "Tamil": "ta"}

# ---- DOCUMENT GENERATION ----
st.header("Legal Document Generator")
doc_type = st.selectbox("Select Document Type", ["Police Complaint", "RTI Request", "Consumer Complaint", "Legal Notice"])
name = st.text_input("Your Name")
address = st.text_area("Your Address")
details = st.text_area("Describe Your Complaint/Request")

if st.button("Generate Document"):
    if name and address and details:
        prompt = f"Generate a {doc_type} for {name}, living at {address}. Details: {details}"
        generated_text = generate_legal_text(prompt)
        pdf_path = create_pdf(generated_text, "legal_document")
        
        st.success("Document generated successfully!")
        with open(pdf_path, "rb") as file:
            st.download_button("Download PDF", file, file_name="legal_document.pdf", mime="application/pdf")
    else:
        st.error("Please fill in all fields.")

# ---- OCR IMAGE UPLOAD ----
st.header("Text Extraction from Image (OCR)")
uploaded_image = st.file_uploader("Upload an image containing text (Hindi, Tamil, or English)", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    extracted_text = extract_text_from_image(image)
    st.subheader("Extracted Text")
    st.write(extracted_text)

    # Translation
    target_language = lang_map[language]
    translated_text = translate_text(extracted_text, target_language)
    st.subheader(f"Translated Text ({language})")
    st.write(translated_text)

    # Summarization
    summarized_text = summarize_text(translated_text)
    st.subheader("Summarized Text")
    st.write(summarized_text)

# ---- EMAIL LINK ----
st.header("Email Interface")
st.write("Click the button below to access Gmail.")

if st.button("Open Gmail"):
    st.markdown("[Click here to open Gmail](https://mail.google.com/)", unsafe_allow_html=True)

# ---- FOOTER ----
st.write("Developed by AI & ML Enthusiast 🚀")







