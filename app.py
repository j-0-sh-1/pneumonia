import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("Legal Issue Analyzer ⚖️")
st.write("Enter your legal issue, and the system will classify it and find relevant law sections/articles.")

# --- USER INPUT ---
user_input = st.text_area("Describe your legal issue:", height=150)

if st.button("Analyze Issue"):
    if user_input.strip() == "":
        st.warning("Please enter a description before submitting.")
    else:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # --- LEGAL ISSUE CLASSIFICATION ---
        classification_prompt = f"Classify the following legal issue into a complaint type: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
        classification_payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": classification_prompt}]}
        
        classification_response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(classification_payload))
        classification_result = classification_response.json()
        
        # --- LAW SECTION & ARTICLE IDENTIFICATION ---
        law_prompt = f"Identify the relevant legal sections and articles that apply to this issue: {user_input}"
        law_payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": law_prompt}]}
        
        law_response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(law_payload))
        law_result = law_response.json()
        
        # --- DISPLAY RESULTS ---
        if "choices" in classification_result and "choices" in law_result:
            classification_output = classification_result["choices"][0]["message"]["content"]
            law_output = law_result["choices"][0]["message"]["content"]
            
            st.subheader("Classification Result:")
            st.success(classification_output)
            
            st.subheader("Applicable Law Sections & Articles:")
            st.info(law_output)
        else:
            st.error("Error analyzing the issue. Please try again.")
