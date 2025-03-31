import streamlit as st
import pytesseract
from PIL import Image
from googletrans import Translator
from transformers import pipeline
import os

# Set up models
translator = Translator()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Streamlit page config
st.set_page_config(page_title="Image OCR & Summarization", layout="wide")
st.title("📄 Image Text Extraction & Translation Tool")

# File uploader
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Extract text from image
    extracted_text = pytesseract.image_to_string(image, lang="hin+tam+eng").strip()
    st.subheader("Extracted Text:")
    st.text_area("", extracted_text, height=200)
    
    # Translation
    target_language = st.selectbox("Translate To", ["en", "hi", "ta"])
    if st.button("Translate Text"):
        translated_text = translator.translate(extracted_text, dest=target_language).text
        st.subheader("Translated Text:")
        st.text_area("", translated_text, height=200)
    
    # Summarization
    if st.button("Summarize Text"):
        if extracted_text:
            summary = summarizer(extracted_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            st.subheader("Summarized Text:")
            st.text_area("", summary, height=150)
        else:
            st.warning("No text extracted to summarize!")
