import streamlit as st
import requests
import os
from dotenv import load_dotenv
import PyPDF2
import io
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()

# Gemini API Endpoint
# Using gemini-2.0-flash-exp or gemini-1.5-flash as 2.5 might not be available via public endpoint yet?
# User asked for gemini-2.5-flash. I will try that first.
# If it fails, I might need to fallback.
MODEL_NAME = "gemini-2.5-flash" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

st.set_page_config(page_title="Gemini File Chat", page_icon="🤖")

st.title("🤖 Gemini Chat with File Context")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_content" not in st.session_state:
    st.session_state.file_content = ""

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Files")
    uploaded_files = st.file_uploader("Choose PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True)
    
    if uploaded_files:
        all_content = []
        try:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                    all_content.append(f"=== File: {uploaded_file.name} ===\n{text}\n")
                elif uploaded_file.type == "text/plain":
                    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                    content = stringio.read()
                    all_content.append(f"=== File: {uploaded_file.name} ===\n{content}\n")
            
            st.session_state.file_content = "\n".join(all_content)
            st.success(f"{len(uploaded_files)} file(s) loaded successfully!")
        except Exception as e:
            st.error(f"Error reading files: {e}")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something about the file..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload for Gemini API
    contents = []
    
    # Add system instruction / context as the first part of the conversation or system instruction
    # For generateContent, we can just prepend context to the history or use system_instruction if supported.
    # Simple approach: Prepend context to the first user message or just include it in the current turn if it's single turn?
    # But we want chat history.
    
    # Let's construct the full history for the API
    # If file content exists, we can add it as a system instruction or just the first user message.
    
    if st.session_state.file_content:
        system_instruction = f"You are a helpful assistant. Use the following file content as context for the conversation:\n\n{st.session_state.file_content}"
        # We can try to send it as a 'user' message first, or use system_instruction field if using v1beta.
        # Let's try adding it to the first user message in the history we send.
    else:
        system_instruction = "You are a helpful assistant."

    # Construct contents
    # We need to map our role 'assistant' to 'model' for Gemini
    
    # First message with context
    if st.session_state.file_content:
        contents.append({
            "role": "user",
            "parts": [{"text": f"{system_instruction}\n\nUser: {st.session_state.messages[0]['content']}"}]
        })
        # Skip the first message in the loop if we just added it
        start_index = 1
    else:
        start_index = 0

    for i in range(start_index, len(st.session_state.messages)):
        msg = st.session_state.messages[i]
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192,
        }
    }


    with st.spinner("답변을 생성하는 중..."):
        try:
            response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                # Extract text from response
                try:
                    response_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    with st.chat_message("assistant"):
                        st.markdown(response_text)
                except (KeyError, IndexError) as e:
                     st.error(f"Error parsing response: {result}")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Error generating response: {e}")

