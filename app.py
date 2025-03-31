import streamlit as st
import requests
import os

# Load Mistral API Key (Set this in environment variables)
MISTRAL_API_KEY = os.getenv(""Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"")

# API Request Function
def mistral_generate(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-large",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error in AI response")

# Complaint Classification & Email ID Mapping
def classify_complaint(complaint_text):
    categories = {
        "police": "police-helpdesk@gov.com",
        "RTI": "rti-officer@gov.com",
        "consumer": "consumer-forum@gov.com"
    }

    # Ask Mistral API to classify the complaint
    classification_prompt = f"Classify the following complaint into 'police', 'RTI', or 'consumer':\n\n{complaint_text}"
    classification = mistral_generate(classification_prompt).strip().lower()

    return classification, categories.get(classification, "unknown@example.com")

# Generate Step-by-Step Email Guide
def generate_email_guide(complaint_type, email_id, details):
    prompt = f"""
    You are an AI guide for writing emails. Provide a clear, step-by-step guide for writing a complaint email.

    Complaint Type: {complaint_type}
    Authority Email ID: {email_id}
    Complaint Details: {details}

    Steps should be well-structured and easy to follow.
    """
    
    return mistral_generate(prompt)

# Streamlit UI
st.title("AI Email Complaint Assistant 📧")
st.write("Enter your complaint details, and AI will guide you on how to draft and send an email.")

# User Input
complaint_text = st.text_area("Enter Complaint Details")

if st.button("Generate Email Guide"):
    if complaint_text:
        complaint_type, email_id = classify_complaint(complaint_text)
        email_guide = generate_email_guide(complaint_type, email_id, complaint_text)
        
        st.subheader("Step-by-Step Email Guide:")
        st.write(email_guide)
        
        st.subheader("Complaint Type:")
        st.write(complaint_type.title())
        
        st.subheader("Authority Email ID:")
        st.write(email_id)
    else:
        st.error("Please enter complaint details.")


