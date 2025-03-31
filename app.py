import streamlit as st
import requests
import json

# --- MISTRAL API CONFIG ---
MISTRAL_API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"  # Replace with actual API key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.title("⚖️ Legal Navigator Chatbot")
st.write("Chat with a legal assistant to understand your legal rights.")

# --- SESSION STATE FOR CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on legal issues. Provide clear and actionable advice."}
    ]

# --- USER INPUT ---
user_input = st.text_area("📝 Describe your issue or ask a legal question:", height=150)

if st.button("Send Message"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a message before submitting.")
    else:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call Mistral API
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-medium",
            "messages": st.session_state.messages
        }
        
        response = requests.post(MISTRAL_API_URL, headers=headers, data=json.dumps(payload))
        result = response.json()

        if "choices" in result:
            bot_reply = result["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

            # --- DISPLAY CHAT HISTORY ---
            st.subheader("💬 Chat History")
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.write(f"👤 **You:** {msg['content']}")
                elif msg["role"] == "assistant":
                    st.write(f"🤖 **Legal Assistant:** {msg['content']}")

        else:
            st.error("❌ Error fetching response. Please try again.")

# --- ANALYZE ISSUE AND GENERATE COMPLAINT FORMAT ---
st.subheader("📑 Legal Issue Analysis & Complaint Format")

if st.button("Analyze Issue"):
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
        
       # Show raw API response
           
        try:
            result = response.json()
            st.write("🔍 Debug API Response:", result)  # Show raw API response
  
            if "choices" in result:
                complaint_type = result["choices"][0]["message"]["content"]
                st.success(f"✅ Your issue is classified as: **{complaint_type}**")
            elif "error" in result:
                st.error(f"❌ API Error: {result['error']}")
            else:
                st.error("⚠️ Unexpected API response format.")

        except Exception as e:
            st.error(f"❌ JSON Parsing Error: {e}")

# --- RESET BUTTON TO CLEAR CHAT ---
if st.button("Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on legal issues. Provide clear and actionable advice."}
    ]
    st.success("✅ Chat history cleared!")
