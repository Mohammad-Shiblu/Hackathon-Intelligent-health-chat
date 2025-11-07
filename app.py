"""Main Streamlit application for AI Health Chatbot."""

import streamlit as st
from PIL import Image
import io
from PyPDF2 import PdfReader
from document_analyzer import DocumentAnalyzer
from chat_handler import ChatHandler


# Page configuration
st.set_page_config(
    page_title="AI Health Companion",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize modules
@st.cache_resource
def get_analyzer():
    """Initialize document analyzer (cached)."""
    return DocumentAnalyzer()

@st.cache_resource
def get_chat_handler():
    """Initialize chat handler (cached)."""
    return ChatHandler()

analyzer = get_analyzer()
chat_handler = get_chat_handler()

# Custom CSS for ChatGPT-like UI
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Fixed input at bottom */
    .stChatFloatingInputContainer {
        position: fixed;
        bottom: 0;
        background-color: white;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Compact header */
    .main-header {
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-bottom: 150px;
    }
</style>
""", unsafe_allow_html=True)

# Compact header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("🏥")
with col2:
    st.markdown("### AI Health Companion")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    **AI Health Companion** helps you understand medical documents using:
    - 🤖 Claude 3 Sonnet AI
    - 🔍 Amazon Textract OCR
    - 📚 Medical Knowledge Base
    """)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.info("""
    **💡 How to use:**
    1. Attach a medical document
    2. Type your question
    3. Get instant analysis
    
    **Examples:**
    - "Briefly explain this"
    - "What are the key findings?"
    - "Summarize the results"
    - "Is anything abnormal?"
    """)

# Welcome message if no chat history
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; max-width: 600px; margin: 0 auto;">
        <h2>👋 Welcome to AI Health Companion!</h2>
        <p style="color: #666; margin: 1rem 0;">I can help you understand medical documents and answer health questions.</p>
        <div style="text-align: left; margin-top: 2rem;">
            <p><strong>I can help you:</strong></p>
            <ul style="color: #666;">
                <li>📄 Understand prescriptions and medications</li>
                <li>🧪 Explain lab reports and test results</li>
                <li>🩻 Interpret medical images</li>
                <li>💊 Answer general health questions</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fixed bottom input area
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# File upload (compact)
chat_uploaded_file = st.file_uploader(
    "📎 Attach document",
    type=['jpg', 'jpeg', 'png', 'webp', 'pdf'],
    key="chat_file_uploader",
    label_visibility="collapsed"
)

if chat_uploaded_file:
    st.caption(f"✅ {chat_uploaded_file.name}")

# Chat input using native Streamlit chat input
if prompt := st.chat_input("💬 Ask about your health or medical documents..."):
    # Check if file is attached
    if chat_uploaded_file:
        # Process the attached file
        chat_uploaded_file.seek(0)
        
        # Add user message with file info
        user_message = f"📎 **Attached:** {chat_uploaded_file.name}\n\n{prompt}"
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # Process file based on type
        with st.chat_message("assistant"):
            with st.spinner("Analyzing document..."):
                file_type = chat_uploaded_file.type
                
                if file_type == 'application/pdf':
                    # Extract PDF text
                    pdf_reader = PdfReader(chat_uploaded_file)
                    text_content = ""
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
                    
                    # Analyze with user's custom prompt
                    response = chat_handler.get_response(
                        user_message=f"{prompt}\n\nDocument content:\n{text_content[:4000]}"
                    )
                else:
                    # Extract image data
                    image_data = chat_uploaded_file.read()
                    
                    # Use Textract to extract text
                    from textract_extractor import TextractExtractor
                    textract = TextractExtractor()
                    extracted = textract.extract_structured_data(image_data)
                    
                    # Build context
                    context = f"Extracted text: {extracted['raw_text']}\n\n"
                    if extracted['tables']:
                        context += "Tables found:\n"
                        for i, table in enumerate(extracted['tables'], 1):
                            context += f"Table {i}: {table}\n"
                    
                    # Analyze with user's custom prompt
                    response = chat_handler.get_response(
                        user_message=f"{prompt}\n\n{context}"
                    )
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    else:
        # No file attached - regular chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_handler.get_response(
                    user_message=prompt
                )
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


