# AI Health Companion Chatbot 🏥

An intelligent, modular health chatbot powered by Amazon Bedrock that analyzes medical documents, categorizes images, and explains health information to patients in simple terms.

## Features

- 🤖 **AI-Powered Chat**: Natural conversations about health using Claude 3 Sonnet
- 📄 **Document Analysis**: Automatically categorizes uploaded images as:
  - Prescriptions
  - Lab Reports
  - Medical Images (X-rays, MRI, CT scans)
- 🔍 **Robust OCR**: Amazon Textract extracts text, tables, and key-value pairs from medical documents
- 📊 **Structured Data Extraction**: Handles complex lab reports with tables and forms
- 💬 **Patient-Friendly**: Simple language, empathetic responses
- 🏗️ **Modular Architecture**: Clean, maintainable code structure

## Architecture

```
├── app.py                  # Main Streamlit UI
├── bedrock_client.py       # AWS Bedrock API wrapper
├── textract_extractor.py   # Amazon Textract OCR integration
├── document_analyzer.py    # Document categorization & analysis
├── chat_handler.py         # Conversational AI logic
├── config.py              # Configuration & constants
└── requirements.txt       # Python dependencies
```

## Module Overview

### 1. config.py
- Centralizes all configuration settings
- AWS credentials and region
- Model parameters (temperature, max tokens)
- Document category definitions

### 2. bedrock_client.py
- Handles all AWS Bedrock API calls
- Methods:
  - `invoke_text()`: Text-only interactions
  - `invoke_with_image()`: Image + text analysis

### 3. textract_extractor.py
- Amazon Textract integration for OCR
- Methods:
  - `extract_text()`: Basic text extraction
  - `extract_structured_data()`: Extracts forms, tables, key-value pairs

### 4. document_analyzer.py
- Core document processing logic
- Methods:
  - `categorize_document()`: Identifies document type
  - `explain_prescription()`: Explains medications (uses Textract)
  - `explain_lab_report()`: Interprets test results (uses Textract)
  - `explain_medical_image()`: Describes medical scans
  - `analyze_document()`: Complete analysis pipeline

### 5. chat_handler.py
- Manages patient conversations
- Maintains empathetic, helpful tone
- Provides context-aware responses

### 6. app.py
- Streamlit UI implementation
- Integrates all modules
- Manages session state and user interactions

## Installation

### Prerequisites
- Python 3.8+
- AWS Account with Bedrock access
- Claude 3 Sonnet model enabled

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
cp .env.example .env
# Edit .env with your AWS credentials

# Run the application
streamlit run app.py
```

## AWS Configuration

1. **Enable Amazon Bedrock**:
   - Go to AWS Console → Bedrock
   - Request model access for Claude 3 Sonnet

2. **Enable Amazon Textract**:
   - Textract is available by default in most regions
   - No model access request needed

3. **IAM Permissions**:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "bedrock:Retrieve",
           "textract:DetectDocumentText",
           "textract:AnalyzeDocument"
         ],
         "Resource": [
           "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
           "arn:aws:bedrock:*:*:knowledge-base/*",
           "*"
         ]
       }
     ]
   }
   ```

3. **Set Environment Variables**:
   ```bash
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_DEFAULT_REGION=us-east-1
   KNOWLEDGE_BASE_ID=your_kb_id  # Optional
   ```

4. **Knowledge Base Setup** (Optional):
   - See [KNOWLEDGE_BASE_SETUP.md](KNOWLEDGE_BASE_SETUP.md) for detailed instructions
   - Create knowledge base with medical documents
   - Add Knowledge Base ID to `.env`

## Usage

1. **Start the app**: `streamlit run app.py`
2. **Upload document**: Use sidebar to upload prescription/lab report/medical image
3. **Analyze**: Click "Analyze Document" button
4. **Chat**: Ask questions about the document or general health topics
5. **Get explanations**: Receive clear, patient-friendly responses

## Supported Image Formats

- JPEG/JPG
- PNG
- WEBP

## Document Categories

The AI automatically categorizes uploads into:
- **Prescription**: Medication lists, dosage instructions
- **Lab Report**: Blood tests, pathology results
- **Medical Image**: X-rays, MRI, CT scans, ultrasounds

## Security & Privacy

- Never stores uploaded documents permanently
- Uses AWS secure infrastructure
- No data retention after session ends
- For demonstration purposes only - not for actual medical use

## Technology Stack

- **Frontend**: Streamlit
- **AI Model**: Amazon Bedrock (Claude 3 Sonnet)
- **Cloud**: AWS
- **Language**: Python 3.8+
- **Image Processing**: Pillow

## Limitations

- This is a demonstration application
- Not a substitute for professional medical advice
- Always consult healthcare providers for medical decisions
- Image quality affects analysis accuracy

## Future Enhancements

- Multi-language support
- Voice input/output
- PDF document support
- Medical history tracking
- Integration with EHR systems

## License

Educational/Demonstration purposes only.
