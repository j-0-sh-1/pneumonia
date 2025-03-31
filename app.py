import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"  # Replace with your actual API key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("📑 Legal Issue Classifier")
st.write("Enter your legal issue, and we'll determine the appropriate complaint format.")

# --- USER INPUT ---
user_input = st.text_area("📝 Describe your issue:", height=150)

if st.button("Classify Issue"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a legal issue before analyzing.")
    else:
        analyze_prompt = f"Classify the following legal issue and suggest the best format (Consumer Complaint, RTI Request, Legal Notice, etc.): {user_input}"
        
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-medium",
            "messages": [{"role": "user", "content": analyze_prompt}]
        }

        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        
        try:
            result = response.json()
            st.write("🔍 Debug API Response:", result)  # Show raw API response for debugging
            
            if "choices" in result:
                complaint_type = result["choices"][0]["message"]["content"]
                st.success(f"✅ Your issue is classified as: **{complaint_type}**")
            elif "error" in result:
                st.error(f"❌ API Error: {result['error']}")
            else:
                st.error("⚠️ Unexpected API response format.")

        except Exception as e:
            st.error(f"❌ JSON Parsing Error: {e}")
