import streamlit as st
import requests
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Brain Checker Bot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.3s ease-in;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .status-info {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #c8e6c9;
        border-left: 4px solid #4caf50;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_URL = "http://localhost:8000"

# Initialize session state
if "messages" in st.session_state:
    pass
else:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.markdown("# 🧠 Brain Checker Bot")
st.markdown("Your interactive AI assistant for Brain Checker counseling reports")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📄 Upload & Process")
    
    uploaded_file = st.file_uploader(
        "Upload your Brain Checker PDF report",
        type="pdf",
        help="Select a PDF file to process"
    )
    
    if uploaded_file is not None:
        if st.button("📤 Process PDF", use_container_width=True):
            with st.spinner("Processing your PDF..."):
                try:
                    # Upload file to backend
                    files = {"file": (uploaded_file.name, uploaded_file.getbuffer(), "application/pdf")}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.session_state.pdf_uploaded = True
                        st.success("✅ PDF processed successfully!")
                        st.session_state.messages = []  # Clear chat history on new PDF
                    else:
                        st.error(f"❌ Error uploading PDF: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend. Make sure FastAPI is running on http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    st.markdown("### Status")
    if st.session_state.pdf_uploaded:
        st.info("✅ PDF loaded and ready for questions", icon="ℹ️")
    else:
        st.warning("⚠️ No PDF uploaded yet. Please upload a PDF to start.", icon="⚠️")
    
    st.divider()
    st.markdown("### Instructions")
    st.markdown("""
    1. Upload your Brain Checker report PDF
    2. Wait for processing to complete
    3. Ask questions in the chat area
    4. Get AI-powered insights based on your report
    """)

# Main chat area
if st.session_state.pdf_uploaded:
    st.subheader("💬 Chat with AI Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><b>Assistant:</b> {message["content"]}</div>', 
                           unsafe_allow_html=True)
    
    # Input area
    st.divider()
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask a question about your report",
            placeholder="e.g., What does my IQ score indicate?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True)
    
    # Process user input
    if send_button and user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Get bot response
        with st.spinner("⏳ AI is thinking (this may take 30-120 seconds on slower hardware)..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": user_input},
                    timeout=180  # Increased to 3 minutes for slow laptops
                )
                
                if response.status_code == 200:
                    bot_answer = response.json().get("answer", "No response generated")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_answer
                    })
                    st.rerun()
                else:
                    st.error(f"❌ Error getting response: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The model might be taking too long.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

else:
    # Welcome screen
    st.info("👈 Please upload a PDF report in the sidebar to get started", icon="ℹ️")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📚 Learn")
        st.write("Upload your Brain Checker counseling report to begin")
    
    with col2:
        st.markdown("### 💡 Ask")
        st.write("Ask any question about your test results")
    
    with col3:
        st.markdown("### 📊 Understand")
        st.write("Get detailed explanations based on your report")
