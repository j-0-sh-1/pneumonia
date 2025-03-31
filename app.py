import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("Legal Issue Classifier ⚖️")
st.write("Enter your legal issue, and the system will classify it into a relevant complaint type.")

# --- USER INPUT ---
user_input = st.text_area("Describe your legal issue:", height=150)

if st.button("Classify Issue"):
    if user_input.strip() == "":
        st.warning("Please enter a description before submitting.")
    else:
        # --- MISTRAL API CALL ---
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Classify the following legal issue into a complaint type: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
        
        payload = {
            "model": "mistral-medium",  # Choose an appropriate model
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        result = response.json()

        # --- DISPLAY CLASSIFICATION RESULT ---
        if "choices" in result:
            classification_result = result["choices"][0]["message"]["content"]
            st.subheader("Classification Result:")
            st.success(classification_result)  # Shows only the classification result
        else:
            st.error("Error analyzing the issue. Please try again.")

