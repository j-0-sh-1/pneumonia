import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("Legal Issue Analyzer ⚖️")
st.write("Enter your legal issue, and the system will classify it into a relevant complaint type and identify applicable legal provisions.")

# --- USER INPUT ---
user_input = st.text_area("Describe your legal issue:", height=150)

if st.button("Analyze Issue"):
    if user_input.strip() == "":
        st.warning("Please enter a description before submitting.")
    else:
        # --- MISTRAL API CALL FOR CLASSIFICATION ---
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        classification_prompt = (
            f"Classify the following legal issue into a complaint type: {user_input}\n"
            "Options: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
        )
        
        classification_payload = {
            "model": "mistral-medium",
            "messages": [{"role": "user", "content": classification_prompt}]
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(classification_payload))
        result = response.json()

        if "choices" in result:
            classification_result = result["choices"][0]["message"]["content"]
            st.subheader("Classification Result:")
            st.success(classification_result)
        else:
            st.error("Error analyzing the issue. Please try again.")

        # --- MISTRAL API CALL FOR LEGAL SECTIONS ---
        section_prompt = (
            f"Identify the relevant sections, articles, or laws under the Indian Constitution that apply to the following legal issue: {user_input}"
        )
        
        section_payload = {
            "model": "mistral-medium",
            "messages": [{"role": "user", "content": section_prompt}]
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(section_payload))
        result = response.json()

        if "choices" in result:
            section_result = result["choices"][0]["message"]["content"]
            st.subheader("Relevant Legal Provisions:")
            st.info(section_result)
        else:
            st.error("Error retrieving legal sections. Please try again.")
