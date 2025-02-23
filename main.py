import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Medi.ai!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key="AIzaSyDBVRi6017VGCToebo2d4rhQ-b_DbHSqaQ")
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("Medi.ai - ChatBot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask about diseases and symptoms related query ...")
if user_prompt:
    # Add instruction to restrict responses to disease-specific topics
    disease_prompt = (
        "You are a medical assistant. Only answer queries related to hello, thank you, diseases, symptoms, treatments,medications and health conditions. "
        "If the question is unrelated to diseases, respond with: 'I can only provide disease-related information.'.\n\n"
        f"User: {user_prompt}"
    )

    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send modified query to Gemini-Pro
    gemini_response = st.session_state.chat_session.send_message(disease_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)