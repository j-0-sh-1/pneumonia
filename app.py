import streamlit as st
import requests
import json

# --- CONFIGURATION ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Legal Navigator Chatbot", page_icon="⚖️")
st.markdown("""
    <style>
    .chat-box {border-radius: 10px; padding: 10px; margin-bottom: 5px;}
    .user-box {background-color: #DCF8C6; align-self: flex-end;}
    .assistant-box {background-color: #E8E8E8;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("ℹ️ Instructions")
st.sidebar.write("Ask legal questions and receive guidance from the assistant.")
st.sidebar.markdown("✅ Get step-by-step legal advice\n✅ Receive useful links for action\n✅ Easily reset the chat")

st.title("Legal Navigator Chatbot 🤖⚖️")
st.write("_Chat with a legal assistant to understand your legal rights._")

# --- SESSION STATE FOR CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."}
    ]

# --- DISPLAY CHAT HISTORY ---
st.subheader("📝 Chat History")
chat_container = st.container()

for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_container.markdown(f'<div class="chat-box user-box"><b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        chat_container.markdown(f'<div class="chat-box assistant-box"><b>Legal Assistant:</b> {msg["content"]}</div>', unsafe_allow_html=True)

# --- USER INPUT ---
user_input = st.text_area("🔍 Describe your issue or ask a legal question:", height=150)

if st.button("Send 📨"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a message before submitting.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call Mistral API
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "mistral-medium", "messages": st.session_state.messages}
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            chat_container.markdown(f'<div class="chat-box assistant-box"><b>Legal Assistant:</b> {bot_reply}</div>', unsafe_allow_html=True)

            # --- ACTION SUGGESTIONS ---
            with st.expander("💡 Suggested Actions"):
                if "email" in bot_reply.lower():
                    st.markdown("📧 [Click to Open Gmail](https://mail.google.com)")
                if "portal" in bot_reply.lower():
                    st.markdown("🔗 [Click to Open Legal Portal](https://eservices.tnpolice.gov.in)")
        else:
            st.error("❌ Error fetching response. Please try again.")

# --- RESET CHAT BUTTON ---
if st.button("🔄 Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."}
    ]
    st.success("✅ Chat history cleared!")
