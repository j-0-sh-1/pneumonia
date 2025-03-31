import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "your_api_key_here"  # Replace with your Mistral API Key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  # Fixed URL

# --- STREAMLIT UI ---
st.title("📧 AI Email Drafting Assistant")
st.write("Let AI guide you in composing an email step-by-step.")

# --- SESSION STATE FOR CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant that helps users compose emails by guiding them step by step."}
    ]

# --- USER INPUT FORM ---
st.subheader("📌 Fill in Email Details")
to_email = st.text_input("To:")
subject = st.text_input("Subject:")
body = st.text_area("Body:")

if st.button("✉️ Generate Email Draft"):
    if not to_email or not subject or not body:
        st.warning("⚠️ Please fill in all fields before submitting.")
    else:
        user_input = f"Compose an email with:\nTo: {to_email}\nSubject: {subject}\nBody: {body}"
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call Mistral API
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-medium",  # Select the model
            "messages": st.session_state.messages  # Send chat history
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))

        # ✅ API STATUS CHECK
        st.write("🔍 API Status Code:", response.status_code)

        if response.status_code == 200:
            try:
                result = response.json()
                if "choices" in result:
                    bot_reply = result["choices"][0]["message"]["content"]
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                    # --- DISPLAY RESPONSE ---
                    st.subheader("📩 AI-Generated Email Draft")
                    st.write(f"**To:** {to_email}")
                    st.write(f"**Subject:** {subject}")
                    st.write(f"**Body:**\n{bot_reply}")

                    # --- OPEN GMAIL LINK ---
                    st.write("💡 Suggested Action: Open Gmail to finalize your draft")
                    st.markdown('[📬 Click to Open Gmail](https://mail.google.com)')

                else:
                    st.error("⚠️ Unexpected API response format.")
            except json.JSONDecodeError:
                st.error("⚠️ Error: Unable to parse API response. Check API key & retry.")
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")

# --- RESET BUTTON TO CLEAR CHAT ---
if st.button("🔄 Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant that helps users compose emails by guiding them step by step."}
    ]
    st.success("✅ Chat history cleared!")
