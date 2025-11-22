import os
import base64
import io
from openai import OpenAI
from typing import BinaryIO, Union
from PIL import Image
import fitz

AI_INTEGRATIONS_OPENAI_API_KEY = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
AI_INTEGRATIONS_OPENAI_BASE_URL = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")

def get_openai_client():
    return OpenAI(
        api_key=AI_INTEGRATIONS_OPENAI_API_KEY,
        base_url=AI_INTEGRATIONS_OPENAI_BASE_URL
    )

def transcribe_audio(audio_file: BinaryIO, filename: str = "audio.mp3") -> dict:
    """
    Transcribe audio file to text using OpenAI Whisper.
    
    Args:
        audio_file: Binary file object containing audio data
        filename: Name of the audio file (used for format detection)
    
    Returns:
        dict with 'text' key containing transcription or 'error' key if failed
    """
    try:
        client = get_openai_client()
        
        # Whisper API requires the file to have a name attribute
        audio_file.name = filename
        
        # Call Whisper API
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        
        return {
            "text": transcription,
            "success": True
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def encode_image_to_base64(image_data: bytes) -> str:
    """
    Encode image bytes to base64 string.
    
    Args:
        image_data: Image data as bytes
    
    Returns:
        Base64 encoded string
    """
    return base64.b64encode(image_data).decode('utf-8')

def pdf_to_images(pdf_bytes: bytes, max_pages: int = 5) -> list:
    """
    Convert PDF pages to images.
    
    Args:
        pdf_bytes: PDF file as bytes
        max_pages: Maximum number of pages to process
    
    Returns:
        List of image bytes
    """
    images = []
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # Process up to max_pages
        num_pages = min(len(pdf_document), max_pages)
        
        for page_num in range(num_pages):
            page = pdf_document[page_num]
            
            # Render page to image (higher resolution for better OCR)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            
            # Convert to bytes
            img_bytes = pix.tobytes("png")
            images.append(img_bytes)
        
        pdf_document.close()
        return images
    
    except Exception as e:
        raise Exception(f"Failed to convert PDF to images: {str(e)}")

def extract_text_from_image(image_bytes: bytes, file_type: str = "image") -> dict:
    """
    Extract text from an image using OpenAI Vision API.
    
    Args:
        image_bytes: Image data as bytes
        file_type: Type of file (image or pdf) for context
    
    Returns:
        dict with 'text' key containing extracted text or 'error' key if failed
    """
    try:
        client = get_openai_client()
        
        # Encode image to base64
        base64_image = encode_image_to_base64(image_bytes)
        
        # Prepare the prompt
        if file_type.lower() == "pdf" or file_type.lower() == "lab_report":
            prompt = """Extract all text from this medical lab report or document. 
Include all patient information, test names, values, reference ranges, and any clinical notes.
Preserve the structure and formatting as much as possible.
Format the output as clear, readable text that can be used for medical documentation."""
        else:
            prompt = """Extract all text from this medical document or image.
Include all relevant medical information, preserving structure and formatting.
Format the output as clear, readable text."""
        
        # Call Vision API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        extracted_text = response.choices[0].message.content
        
        return {
            "text": extracted_text,
            "success": True
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def process_lab_report(file_bytes: bytes, filename: str) -> dict:
    """
    Process a lab report (PDF or image) and extract text using OCR.
    
    Args:
        file_bytes: File data as bytes
        filename: Name of the file (used for format detection)
    
    Returns:
        dict with 'text' key containing extracted text or 'error' key if failed
    """
    try:
        file_ext = filename.lower().split('.')[-1]
        
        if file_ext == 'pdf':
            # Convert PDF to images and extract text from each page
            images = pdf_to_images(file_bytes, max_pages=5)
            
            all_text = []
            for i, img_bytes in enumerate(images):
                result = extract_text_from_image(img_bytes, file_type="pdf")
                if result.get("success"):
                    all_text.append(f"--- Page {i+1} ---\n{result['text']}")
                else:
                    return result
            
            return {
                "text": "\n\n".join(all_text),
                "success": True,
                "pages_processed": len(images)
            }
        
        elif file_ext in ['jpg', 'jpeg', 'png']:
            # Process image directly
            return extract_text_from_image(file_bytes, file_type="lab_report")
        
        else:
            return {
                "error": f"Unsupported file type: {file_ext}",
                "success": False
            }
    
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }
