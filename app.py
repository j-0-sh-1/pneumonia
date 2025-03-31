import streamlit as st
import requests
import pytesseract
from PIL import Image

# Configure Mistral API
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Define complaint categories and corresponding emails/portals
complaint_options = {
    "Consumer Complaint": {"email": "nationalconsumerhelpline@nic.in", "portal": "https://consumerhelpline.gov.in"},
    "Cybercrime": {"email": "cybercrime@police.gov", "portal": "https://cybercrime.gov.in"},
    "Police Complaint": {"email": "acp-southwest-dl@nic.in", "portal": "https://police.gov.in"},
    "RTI Request": {"email": "rtionline@nic.in", "portal": "https://rtionline.gov.in"},
    "Income Tax Complaint": {"email": "ask@incometax.gov.in", "portal": "https://www.incometax.gov.in"},
    "Human Rights Violation": {"email": "covid19.complaints@nhrc.in", "portal": "https://nhrc.nic.in"},
    "Women’s Safety": {"email": "complaints-ncw@nic.in", "portal": "https://ncw.nic.in"}
}

# Function to classify complaint using Mistral API
def classify_complaint(complaint_text):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Classify the following complaint: {complaint_text}\nChoose from: {', '.join(complaint_options.keys())}" 
    data = {"model": "mistral-tiny", "messages": [{"role": "user", "content": prompt}]}
    
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    return "Error: Classification failed."

# Function to extract text from uploaded image
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Streamlit UI
st.title("AI-Powered Legal Assistant")

# Complaint Entry
st.subheader("Enter Your Complaint")
complaint_text = st.text_area("Describe your complaint:")

if st.button("Classify Complaint"):
    if complaint_text:
        category = classify_complaint(complaint_text)
        email = complaint_options.get(category, {}).get("email", "N/A")
        portal = complaint_options.get(category, {}).get("portal", "N/A")
        
        st.success(f"Complaint Category: **{category}**")
        st.info(f"Email: **{email}**")
        st.markdown(f"[Go to Portal]({portal})")
    else:
        st.warning("Please enter a complaint.")

# Upload Document for OCR
st.subheader("Upload a Legal Document (Image)")
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    extracted_text = extract_text_from_image(image)
    st.text_area("Extracted Text:", extracted_text, height=200)

# AI Legal Chatbot
st.subheader("Ask AI Legal Advisor")
user_query = st.text_input("Enter your legal question:")

if st.button("Get Advice"):
    if user_query:
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
        data = {"model": "mistral-medium", "messages": [{"role": "system", "content": "You are a legal advisor."},
                                                           {"role": "user", "content": user_query}]}
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            legal_advice = response.json()["choices"][0]["message"]["content"].strip()
            st.write(legal_advice)
        else:
            st.error("Error retrieving legal advice.")
    else:
        st.warning("Please enter a question.")

# AI Agent Updates
st.subheader("AI Agent Update")
st.text_area("Summary of AI Actions:", "", height=150)
