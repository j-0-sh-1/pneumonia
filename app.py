import streamlit as st
import os
import pdfkit
from mistralai.client import MistralClient

# Load API Key from Environment
MISTRAL_API_KEY = os.environ.get("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")

# Initialize Mistral Client
client = MistralClient(api_key="Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")

# Complaint Categories & Email Mapping
COMPLAINT_EMAILS = {
    "Police Report": "police@official.com",
    "RTI Request": "rti-officer@gov.com",
    "Consumer Complaint": "consumer-helpline@gov.com"
}

def classify_complaint(complaint_text):
    """Classify the complaint type using AI."""
    response = client.generate(
        model="mistral-7b-instruct",
        prompt=f"Classify this complaint: {complaint_text}. Options: Police Report, RTI Request, Consumer Complaint.",
        max_tokens=10
    )
    return response.text.strip()

def generate_email_guide(complaint_type, details):
    """Generate a step-by-step guide to writing the complaint email."""
    email_id = COMPLAINT_EMAILS.get(complaint_type, "support@default.com")
    prompt = f"""
    Write a step-by-step guide on how to write an email for a {complaint_type}.
    Complaint details: {details}
    """
    
    response = client.generate(model="mistral-7b-instruct", prompt=prompt, max_tokens=200)
    return response.text.strip(), email_id

def generate_pdf(content, filename="Complaint_Guide.pdf"):
    """Generate a PDF with the email drafting guide."""
    pdfkit.from_string(content, filename)

def main():
    st.title("AI-Powered Complaint Letter Generator")
    complaint_text = st.text_area("Enter your complaint details:")
    
    if st.button("Generate Complaint Guide"):
        if complaint_text:
            complaint_type = classify_complaint(complaint_text)
            guide, email_id = generate_email_guide(complaint_type, complaint_text)
            
            # Display Output
            st.subheader("Complaint Classification:")
            st.write(f"**Category:** {complaint_type}")
            st.write(f"**Authority Email ID:** {email_id}")
            
            st.subheader("Step-by-Step Email Writing Guide:")
            st.write(guide)
            
            # Generate PDF
            generate_pdf(guide)
            st.download_button(label="Download PDF", data=open("Complaint_Guide.pdf", "rb"), file_name="Complaint_Guide.pdf", mime="application/pdf")
        else:
            st.error("Please enter complaint details.")

if __name__ == "__main__":
    main()



# Load Mistral API Key (Set this in environment variables)
MISTRAL_API_KEY = os.getenv("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")

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


