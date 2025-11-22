import os
from openai import OpenAI
from typing import BinaryIO

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
