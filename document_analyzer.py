"""Document analysis module for categorizing and processing medical documents."""

from bedrock_client import BedrockClient
from config import DOCUMENT_CATEGORIES


class DocumentAnalyzer:
    """Analyzes and categorizes medical documents and images."""
    
    def __init__(self):
        """Initialize with Bedrock client."""
        self.bedrock = BedrockClient()
    
    def categorize_document(self, image_data: bytes, media_type: str) -> dict:
        """
        Categorize uploaded medical document by analyzing its content.
        
        Args:
            image_data: Binary image data
            media_type: Image MIME type
            
        Returns:
            Dictionary with category and confidence
        """
        prompt = """Analyze this medical document and categorize it into ONE of these types:
1. PRESCRIPTION - Contains medication names, dosages, doctor's signature
2. LAB_REPORT - Contains test results, lab values, pathology findings
3. MEDICAL_IMAGE - X-ray, MRI, CT scan, ultrasound, or other diagnostic imaging
4. UNKNOWN - Cannot determine or doesn't fit above categories

Respond with ONLY the category name (PRESCRIPTION, LAB_REPORT, MEDICAL_IMAGE, or UNKNOWN)."""
        
        system_prompt = "You are a medical document classifier. Respond only with the category name."
        
        category = self.bedrock.invoke_with_image(
            prompt=prompt,
            image_data=image_data,
            media_type=media_type,
            system_prompt=system_prompt
        ).strip()
        
        return {
            'category': category if category in DOCUMENT_CATEGORIES.values() else 'unknown',
            'category_display': category
        }
    
    def explain_prescription(self, image_data: bytes, media_type: str) -> str:
        """
        Explain prescription details in patient-friendly language.
        
        Args:
            image_data: Binary prescription image
            media_type: Image MIME type
            
        Returns:
            Detailed explanation of the prescription
        """
        prompt = """Analyze this prescription and explain:
1. Medications prescribed (names and purposes)
2. Dosage instructions in simple terms
3. Duration of treatment
4. Important precautions or side effects
5. When to take each medication

Use simple, patient-friendly language."""
        
        system_prompt = "You are a compassionate healthcare assistant explaining prescriptions to patients."
        
        return self.bedrock.invoke_with_image(
            prompt=prompt,
            image_data=image_data,
            media_type=media_type,
            system_prompt=system_prompt
        )
    
    def explain_lab_report(self, image_data: bytes, media_type: str) -> str:
        """
        Explain lab report results in understandable terms.
        
        Args:
            image_data: Binary lab report image
            media_type: Image MIME type
            
        Returns:
            Detailed explanation of lab results
        """
        prompt = """Analyze this lab report and explain:
1. What tests were performed
2. Key findings and values
3. Which values are normal vs abnormal
4. What abnormal values might indicate
5. General health implications

Use simple language that patients can understand."""
        
        system_prompt = "You are a healthcare assistant explaining lab results to patients in simple terms."
        
        return self.bedrock.invoke_with_image(
            prompt=prompt,
            image_data=image_data,
            media_type=media_type,
            system_prompt=system_prompt
        )
    
    def explain_medical_image(self, image_data: bytes, media_type: str) -> str:
        """
        Explain medical imaging results.
        
        Args:
            image_data: Binary medical image
            media_type: Image MIME type
            
        Returns:
            Explanation of the medical image
        """
        prompt = """Analyze this medical image and explain:
1. Type of imaging (X-ray, MRI, CT, etc.)
2. Body part or area being examined
3. Visible findings or abnormalities
4. What these findings might mean
5. General observations

Use simple, reassuring language."""
        
        system_prompt = "You are a healthcare assistant explaining medical images to patients."
        
        return self.bedrock.invoke_with_image(
            prompt=prompt,
            image_data=image_data,
            media_type=media_type,
            system_prompt=system_prompt
        )
    
    def analyze_document(self, image_data: bytes, media_type: str) -> dict:
        """
        Complete document analysis pipeline: categorize and explain.
        
        Args:
            image_data: Binary image data
            media_type: Image MIME type
            
        Returns:
            Dictionary with category and explanation
        """
        # Step 1: Categorize the document
        categorization = self.categorize_document(image_data, media_type)
        category = categorization['category']
        
        # Step 2: Generate appropriate explanation based on category
        if category == 'prescription':
            explanation = self.explain_prescription(image_data, media_type)
        elif category == 'lab_report':
            explanation = self.explain_lab_report(image_data, media_type)
        elif category == 'medical_image':
            explanation = self.explain_medical_image(image_data, media_type)
        else:
            explanation = "I couldn't clearly identify this document type. Please upload a clear image of a prescription, lab report, or medical scan."
        
        return {
            'category': category,
            'category_display': categorization['category_display'],
            'explanation': explanation
        }
