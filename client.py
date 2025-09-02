# client.py
import streamlit as st
import requests
import json
from typing import Optional
import requests

# Configuration
API_BASE_URL = "http://localhost:8000"

st.write("Upload a file to FastAPI")
file = st.file_uploader("chose a file", type=["pdf"])

if st.button("Submit"):
    if file is not None:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
    else:
        st.write("No file uploaded.")


def send_message_to_api(prompt: str, model: str = "text", temperature: float = 0.7) -> Optional[str]:
    """
    Send a message to the FastAPI /generate/text endpoint
    """
    try:
        payload = {
            "prompt": prompt,
            "model": model,
            "temperature": temperature
        }
        
        response = requests.post(
            f"{API_BASE_URL}/generate/text",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get("content", "No content received")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API server. Make sure the FastAPI server is running on localhost:8000")
        return None
    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out. The API is taking too long to respond.")
        return None
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="AI Text Generator",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 AI Text Generator")
    st.markdown("Send a message to generate AI-powered text responses")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        model = st.selectbox(
            "Select Model",
            ["gpt-3.5-turbo", "gpt-4o"],
            index=0
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make output more creative, lower values make it more focused"
        )
        
        st.markdown("---")
        st.markdown("**API Status:**")
        
        # Check API status
        try:
            health_response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
            if health_response.status_code == 200:
                st.success("✅ API Server is running")
            else:
                st.warning("⚠️ API Server responded with an error")
        except:
            st.error("❌ Cannot connect to API Server")
    
    # Main chat interface
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = send_message_to_api(prompt, model, temperature)
                
                if response:
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Failed to get response from API")
    
    # Clear chat button
    if st.session_state.messages and st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
