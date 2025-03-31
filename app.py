import streamlit as st
import os
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Set Page Config
st.set_page_config(page_title="Multifunctional Legal Tool", layout="wide")

# Initialize Translator
translator = Translator()

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

# Main UI
def main():
    st.title("📜 Multifunctional Legal & OCR Tool")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📧 Email Drafting Assistant", use_container_width=True):
            st.session_state.page = "email_assistant"

    with col2:
        if st.button("📄 Legal Document Generator", use_container_width=True):
            st.session_state.page = "document"

    with col3:
        if st.button("🖼️ Image Extraction", use_container_width=True):
            st.session_state.page = "ocr"

    if "page" in st.session_state:
        if st.session_state.page == "email_assistant":
            st.header("📧 Email Drafting Assistant")
            st.subheader("Classify Issue & Article Generation")
            st.text("This section helps generate articles and classify legal issues.")
            # Add classification logic here
            if st.button("Classify Issue & Generate Article"):
                st.success("Feature coming soon!")

        elif st.session_state.page == "document":
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
                        st.button("📧 File a Complaint via Email")
                else:
                    st.error("Please fill in all fields.")

        elif st.session_state.page == "ocr":
            st.header("🖼️ Text Extraction from Image")
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

if __name__ == "__main__":
    main()
