import streamlit as st
import requests

# Mistral API Key (Replace with your actual API Key)
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL ="https://api.mistral.ai/v1/chat/completions"

# Define complaint categories and corresponding email addresses
complaint_emails = {
    "Consumer Complaint": "consumer@legalhelp.com",
    "Cybercrime": "cybercrime@police.gov",
    "Workplace Harassment": "hr@company.com",
    "Legal Notice": "legal@lawfirm.com",
    "Government Issue": "govhelp@india.gov",
    "Financial Fraud": "fraudreport@bank.com",
    "Intellectual Property Violation": "ip@lawfirm.com",
    "Tenant-Landlord Dispute": "rentals@housing.com",
    "Environmental Complaint": "environment@ngo.org",
    "Medical Negligence": "health@hospital.com"
    "Human Rights Violations (NHRC)": "covid19.complaints@nhrc.in",
    "Women’s Safety & Harassment Complaints": "complaints-ncw@nic.in"
}

# Function to classify complaint using Mistral API
def classify_complaint(complaint_text):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"Classify the following complaint into one of these categories: {', '.join(complaint_emails.keys())}.\nComplaint: {complaint_text}\nCategory:"

    data = {
        "model": "mistral-tiny",  
        "messages": [{"role": "system", "content": "You are a legal expert that classifies complaints."},
                     {"role": "user", "content": prompt}]
    }
    
    response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        classification = result["choices"][0]["message"]["content"].strip()
        return classification
    else:
        return "Error: Unable to classify complaint."

# Streamlit UI
st.title("AI-Powered Complaint Classifier")

complaint_text = st.text_area("Enter your complaint:")

if st.button("Classify Complaint"):
    if complaint_text:
        category = classify_complaint(complaint_text)
        email = complaint_emails.get(category, "No email available for this category")

        st.success(f"Predicted Complaint Category: **{category}**")
        st.info(f"Relevant Email Address: **{email}**")
    else:
        st.warning("Please enter a complaint.")



