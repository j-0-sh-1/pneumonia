import streamlit as st
import pytesseract
from PIL import Image
from googletrans import Translator
from transformers import pipeline

# Initialize translator and summarizer
translator = Translator()
summarizer = pipeline("summarization")

# Streamlit UI
st.set_page_config(page_title="Image Text Extraction & Translation", layout="wide")
st.title("🖼️ Image Text Extraction, Translation & Summarization")

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with st.spinner("Extracting text..."):
        extracted_text = pytesseract.image_to_string(image, lang="hin+tam+eng").strip()
    
    if extracted_text:
        st.subheader("Extracted Text")
        st.text_area("", extracted_text, height=150)
        
        with st.spinner("Translating text..."):
            translated_text = translator.translate(extracted_text, dest="en").text
        
        st.subheader("Translated Text (English)")
        st.text_area("", translated_text, height=150)
        
        if st.button("Summarize Text"):
            with st.spinner("Summarizing text..."):
                summary = summarizer(translated_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
            
            st.subheader("Summarized Text")
            st.write(summary)
    else:
        st.warning("No text could be extracted from the image. Try another image.")
