import streamlit as st
import openai
import os

# Load API Key (Ensure you have OpenAI API key set as an environment variable)
OPENAI_API_KEY = os.getenv("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")

# Function to classify complaint type and find authority email
def classify_complaint(complaint_text):
    categories = {
        "police": "police-helpdesk@gov.com",
        "RTI": "rti-officer@gov.com",
        "consumer": "consumer-forum@gov.com"
    }
    
    # Ask AI to classify the complaint
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Classify the complaint into one of these categories: police, RTI, consumer."},
            {"role": "user", "content": complaint_text}
        ]
    )
    
    classification = response['choices'][0]['message']['content'].strip().lower()
    return classification, categories.get(classification, "unknown@example.com")

# Function to generate AI-generated step-by-step email guide
def generate_email_guide(complaint_type, email_id, details):
    prompt = f"""
    Generate a step-by-step guide to writing an email complaint for {complaint_type}.
    The email should be sent to {email_id}.
    The complaint details: {details}
    Provide a structured paragraph explaining the steps.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that provides structured step-by-step guides."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Streamlit UI
st.title("AI Email Complaint Assistant 📧")
st.write("Enter your complaint details, and the AI will guide you on how to draft and send an email.")

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
