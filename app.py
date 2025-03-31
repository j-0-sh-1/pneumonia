import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Load API Key from .env file
load_dotenv()
MISTRAL_API_KEY = os.getenv("Xnoij9Emwmr745DUVFfE5s66agi9Gsj3")  # Store API key in .env file
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# --- STREAMLIT UI ---
st.set_page_config(page_title="Legal Navigator Chatbot", layout="wide")

st.title("⚖️ Legal Navigator Chatbot")
st.write("Chat with the legal assistant to understand your legal rights and generate complaint documents.")

# --- SESSION STATE FOR CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on legal complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."}
    ]

# --- CHATBOT INTERFACE ---
st.subheader("💬 Chat with Legal Assistant")

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
            st.subheader("📜 Chat History")
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.write(f"**You:** {msg['content']}")
                elif msg["role"] == "assistant":
                    st.write(f"**Legal Assistant:** {msg['content']}")

        else:
            st.error("Error fetching response. Please try again.")

# --- RESET BUTTON TO CLEAR CHAT ---
if st.button("Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a legal assistant that provides guidance on complaints. Offer actionable steps but do not take major actions like submitting forms or sending emails."}
    ]
    st.success("Chat history cleared!")

# --- ISSUE ANALYSIS & COMPLAINT GENERATOR ---
st.subheader("📑 Issue Analyzer & Complaint Generator")
st.write("Analyze your issue and generate a formatted complaint document.")

if st.button("Analyze Issue"):
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
    result = response.json()

    if "choices" in result:
        complaint_type = result["choices"][0]["message"]["content"]
        st.success(f"✅ Your issue is classified as: **{complaint_type}**")

        # Generate Complaint Document
        def create_pdf(text, filename):
            pdf_path = f"downloads/{filename}.pdf"
            os.makedirs("downloads", exist_ok=True)
            c = canvas.Canvas(pdf_path, pagesize=A4)
            c.drawString(100, 800, f"{complaint_type} Document")

            text_lines = text.split("\n")
            y_position = 780
            for line in text_lines:
                if y_position < 50:
                    c.showPage()
                    y_position = 800
                c.drawString(50, y_position, line)
                y_position -= 20

            c.save()
            return pdf_path

        formatted_complaint = f"Generated {complaint_type} for your issue:\n\n{user_input}"
        pdf_path = create_pdf(formatted_complaint, "legal_complaint")

        st.subheader("📄 Generated Complaint Document")
        st.write(formatted_complaint)
        with open(pdf_path, "rb") as file:
            st.download_button("📥 Download Complaint PDF", file, file_name="legal_complaint.pdf", mime="application/pdf")

    else:
        st.error("Error analyzing the issue. Please try again.")
