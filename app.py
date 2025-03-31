import streamlit as st
import pytesseract
from PIL import Image
from googletrans import Translator

def extract_text_from_image(image):
    return pytesseract.image_to_string(image, lang="hin+tam+eng").strip()

def main():
    st.title("🖼️ Image Extraction and Translation")
    
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    translator = Translator()
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        extracted_text = extract_text_from_image(image)
        st.subheader("Extracted Text")
        st.write(extracted_text)
        
        if extracted_text:
            translated_text = translator.translate(extracted_text, dest="en").text
            st.subheader("Translated Text (English)")
            st.write(translated_text)

if __name__ == "__main__":
    main()
