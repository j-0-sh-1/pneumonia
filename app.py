import streamlit as st
import requests
import json

# API Credentials
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def classify_legal_issue(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Classify the following legal issue into a complaint type: {user_input}\nOptions: Consumer Complaint, RTI Request, Legal Notice, Police Complaint, Academic Grievance, Workplace Harassment Complaint."
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "Error analyzing the issue.")

def classify_article(user_input):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Analyze the legal issue: {user_input} and suggest related articles from the Indian Constitution."
    payload = {"model": "mistral-medium", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "Error retrieving related articles.")

def main():
    st.set_page_config(page_title="Legal Assistance Hub", layout="wide")
    st.title("⚖️ Legal Assistance Hub")
    
    st.header("Classify Legal Issue & Find Related Articles")
    user_input = st.text_area("Describe your legal issue:", height=150)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Classify Issue"):
            if user_input.strip():
                classification_result = classify_legal_issue(user_input)
                st.subheader("Classification Result:")
                st.success(classification_result)
            else:
                st.warning("Please enter a description before submitting.")
    
    with col2:
        if st.button("Classify Article"):
            if user_input.strip():
                article_result = classify_article(user_input)
                st.subheader("Relevant Constitutional Articles:")
                st.info(article_result)
            else:
                st.warning("Please enter a description before submitting.")

if __name__ == "__main__":
    main()
