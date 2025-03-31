import streamlit as st
from mistralai.client import MistralClient

# Initialize Mistral API Client
API_KEY = "Xnoij9Emwmr745DUVFfE5s66agi9Gsj3"  # Replace with your actual Mistral API key
client = MistralClient(api_key=API_KEY)

def get_task_algorithm(user_input):
    """Fetches the step-by-step task process using Mistral API."""
    prompt = f"""
    Given the user request: "{user_input}", generate a step-by-step guide on how to perform this task.
    Example:
    If the user wants to draft an email complaint, provide:
    1. Open Gmail
    2. Click Compose
    3. Enter recipient email
    4. Add subject and complaint details
    5. Save as draft
    """
    
    response = client.generate(prompt)
    return response  # Assuming MistralClient's generate method returns text output

# Streamlit Chatbot UI
st.title("📝 AI Task Assistant")
st.write("Enter your request, and AI will generate step-by-step instructions.")

user_input = st.text_input("Describe your task:")
if st.button("Generate Algorithm"):
    if user_input:
        algorithm = get_task_algorithm(user_input)
        st.markdown("### Step-by-Step Guide:")
        st.write(algorithm)
    else:
        st.warning("Please enter a task description.")
