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
if "document_context" not in st.session_state:
    st.session_state.document_context = ""

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


def process_uploaded_file(uploaded_file):
    """
    Process uploaded medical document (image or PDF).
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Analysis results dictionary
    """
    file_type = uploaded_file.type
    
    # Handle PDF files
    if file_type == 'application/pdf':
        with st.spinner("📄 Extracting PDF text..."):
            pdf_reader = PdfReader(uploaded_file)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            # Analyze PDF text content
            response = chat_handler.get_response(
                user_message=f"Analyze this medical document and categorize it (prescription, lab report, or medical document). Then explain the key findings in simple terms:\n\n{text_content[:4000]}"
            )
            
            return {
                'category': 'pdf_document',
                'category_display': 'PDF Document',
                'explanation': response
            }
    
    # Handle image files
    else:
        image_data = uploaded_file.read()
        media_type_map = {
            'image/jpeg': 'image/jpeg',
            'image/jpg': 'image/jpeg',
            'image/png': 'image/png',
            'image/webp': 'image/webp'
        }
        media_type = media_type_map.get(file_type, 'image/jpeg')
        
        with st.spinner("🔍 Analyzing document..."):
            result = analyzer.analyze_document(image_data, media_type)
        
        return result


# UI Layout
st.title("🏥 AI Health Companion")
st.caption("Your friendly assistant for understanding medical documents")

# Sidebar for document upload
with st.sidebar:
    st.header("📤 Upload Medical Document")
    st.markdown("Upload prescription, lab report, or medical image")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['jpg', 'jpeg', 'png', 'webp', 'pdf'],
        help="Supported: JPG, PNG, WEBP, PDF"
    )
    
    if uploaded_file:
        # Display preview based on file type
        if uploaded_file.type == 'application/pdf':
            st.success(f"📄 PDF: {uploaded_file.name}")
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Document", use_column_width=True) # error corrected
        
        # Analyze button
        if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
            uploaded_file.seek(0)  # Reset file pointer
            result = process_uploaded_file(uploaded_file)
            
            # Store context for chat
            st.session_state.document_context = result['explanation']
            
            # Add to chat history
            analysis_message = f"""**📋 Document Analysis**

**Category:** {result['category_display'].replace('_', ' ').title()}

**Explanation:**
{result['explanation']}"""
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": analysis_message
            })
            
            st.success(f"✅ Identified as: {result['category_display'].replace('_', ' ').title()}")
            st.rerun()
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.document_context = ""
        st.rerun()
    
    st.markdown("---")
    st.info("""
    **💡 How to use:**
    1. Upload medical document
    2. Click 'Analyze Document'
    3. Ask questions in chat
    4. Get clear explanations
    """)

# Main chat interface
st.header("💬 Chat with Your Health Companion")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your health or medical documents..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_handler.get_response(
                user_message=prompt,
                context=st.session_state.document_context
            )
            st.markdown(response)
    
    # Add assistant response to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Welcome message if no chat history
if not st.session_state.messages:
    st.info("""
    👋 **Welcome to AI Health Companion!**
    
    I can help you:
    - 📄 Understand prescriptions and medication instructions
    - 🧪 Explain lab reports and test results
    - 🩻 Interpret medical images and scans
    - 💊 Answer general health questions
    - 🤝 Provide friendly health guidance
    
    **Get started:** Upload a medical document or ask me a question!
    """)
