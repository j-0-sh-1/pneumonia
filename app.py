
import streamlit as st
import requests
import json

# Mistral API Key (Replace with your actual API Key)
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Define complaint categories (For reference)
complaint_categories = [
    "Consumer Complaint", "Cybercrime", "Workplace Harassment",
    "Legal Notice", "Government Issue", "Financial Fraud",
    "Intellectual Property Violation", "Tenant-Landlord Dispute",
    "Environmental Complaint", "Medical Negligence"
]

# Function to classify complaint using Mistral API
def classify_complaint(complaint_text):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # Define prompt for classification
    prompt = f"Classify the following complaint into one of these categories: {', '.join(complaint_categories)}.\nComplaint: {complaint_text}\nCategory:"

    data = {
        "model": "mistral-tiny",  # Change model as needed
        "messages": [{"role": "system", "content": "You are a legal expert that classifies complaints."},
                     {"role": "user", "content": prompt}]
    }
    
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        classification = result["choices"][0]["message"]["content"]
        return classification.strip()
    else:
        return "Error: Unable to classify complaint."

# Streamlit UI
st.title("Complaint Classification with Mistral AI")
complaint_text = st.text_area("Enter your complaint:")

if st.button("Classify Complaint"):
    if complaint_text:
        category = classify_complaint(complaint_text)
        st.success(f"Predicted Complaint Category: **{category}**")
    else:
        st.warning("Please enter a complaint.")


