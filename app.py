import pytesseract
from PIL import Image
from googletrans import Translator
from transformers import pipeline
import streamlit as st

# Configure Tesseract (Ensure it's installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this path as needed

# Load summarization model
summarizer = pipeline("summarization")

# Function to extract text from image
def extract_text(image):
    text = pytesseract.image_to_string(image, lang="hin+tam")
    return text.strip()

# Function to translate text to English
def translate_text(text, dest_lang="en"):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text

# Function to summarize text
def summarize_text(text, max_length=100):
    if len(text.split()) > 30:  # Only summarize if text is long enough
        summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    return text  # Return original if too short

# Streamlit UI
st.title("📷 Image Text Extraction & Summarization Tool")

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    extracted_text = extract_text(image)
    st.subheader("Extracted Text")
    st.write(extracted_text)
    
    translated_text = translate_text(extracted_text)
    st.subheader("Translated Text (English)")
    st.write(translated_text)
    
    summarized_text = summarize_text(translated_text)
    st.subheader("Summarized Text")
    st.write(summarized_text)
