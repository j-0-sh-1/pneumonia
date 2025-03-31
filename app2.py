import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("Legal Navigator Chatbot 🤖⚖️")
st.write("Chat with the legal assistant to understand your legal options.")

# --- SESSION STATE FOR CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."}
    ]

# --- USER INPUT ---
user_input = st.text_area("Describe your issue or ask a legal question:", height=150)

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message before submitting.")
    else:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call Mistral API
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-medium",  # Choose an appropriate model
            "messages": st.session_state.messages  # Send chat history
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            # --- DISPLAY CHAT HISTORY ---
            st.subheader("Chat History")
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.write(f"**You:** {msg['content']}")
                elif msg["role"] == "assistant":
                    st.write(f"**Legal Assistant:** {msg['content']}")

            # --- ACTION SUGGESTIONS ---
            if "email" in bot_reply.lower():
                st.write("💡 Suggested Action: Open Gmail for Drafting")
                st.markdown('[Click to Open Gmail](https://mail.google.com)')

            if "portal" in bot_reply.lower():
                st.write("💡 Suggested Action: Visit Legal Portal")
                st.markdown('[Click to Open FIR Portal](https://eservices.tnpolice.gov.in)')

        else:
            st.error("Error fetching response. Please try again.")

# --- RESET BUTTON TO CLEAR CHAT ---
if st.button("Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."}
    ]
    st.success("Chat history cleared!")
