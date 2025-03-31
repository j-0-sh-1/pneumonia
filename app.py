import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("Legal Navigator Chatbot")
st.write("Enter your complaint below to receive legal guidance.")

# --- TEXT INPUT ---
complaint_text = st.text_area("Describe your issue", height=150)

if st.button("Get Legal Advice"):
    if complaint_text.strip() == "":
        st.warning("Please enter a complaint before submitting.")
    else:
        # --- CALL MISTRAL API ---
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-medium",  # Choose an appropriate model
            "messages": [
                {"role": "system", "content": "You are a legal assistant that provides guidance on complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."},
                {"role": "user", "content": f"Here is the complaint: {complaint_text}. What are the next legal steps?"}
            ]
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
            st.success("Legal Guidance:")
            st.write(bot_reply)

            # --- ACTION SUGGESTIONS ---
            if "email" in bot_reply.lower():
                st.write("💡 Suggested Action: Open Gmail for Drafting")
                st.markdown('[Click to Open Gmail](https://mail.google.com)')

            if "portal" in bot_reply.lower():
                st.write("💡 Suggested Action: Visit Legal Portal")
                st.markdown('[Click to Open FIR Portal](https://eservices.tnpolice.gov.in)')
        else:
            st.error("Error fetching response. Please try again.")
