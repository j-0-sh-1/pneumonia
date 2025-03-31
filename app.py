import streamlit as st
import requests
import json
import os
import pytesseract
from PIL import Image
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Set Page Config
st.set_page_config(page_title="Legal Issue Analyzer", layout="wide")
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

st.title("⚖️ Legal Issue Analyzer & Multifunctional Tool")
st.write("Analyze legal issues, generate documents, and extract text from images.")

col1, col2, col3 = st.columns(3)

# --- Legal Issue Classification & Law Sections ---
with col1:
    st.header("🔍 Legal Issue Analyzer")
    user_input = st.text_area("Describe your legal issue:", height=150)
    if st.button("Analyze Issue"):
        if user_input.strip() == "":
            st.warning("Please enter a description before submitting.")
        else:
            headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
            classification_prompt = f"Classify the following legal issue into a complaint type: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
            classification_payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": classification_prompt}]}
            response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(classification_payload))
            result = response.json()
            classification_result = result.get("choices", [{}])[0].get("message", {}).get("content", "Error retrieving classification.")
            st.success(classification_result)
            
            section_prompt = f"Identify the relevant sections, articles, or laws under the Indian Constitution that apply to the following legal issue: {user_input}"
            section_payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": section_prompt}]}
            response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(section_payload))
            result = response.json()
            section_result = result.get("choices", [{}])[0].get("message", {}).get("content", "Error retrieving legal sections.")
            st.info(section_result)

# --- Legal Document Generator ---
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
            
            # Add Email Filing Button
            mailto_link = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su=Legal%20Complaint&body={details.replace(' ', '%20')}"
            st.markdown(f'<a href="{mailto_link}" target="_blank" style="display:inline-block; padding:8px 15px; background:#d93025; color:white; text-decoration:none; border-radius:5px;">📧 File a Complaint via Email</a>', unsafe_allow_html=True)
        else:
            st.error("Please fill in all fields.")

# --- OCR Image Text Extraction ---
with col3:
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
