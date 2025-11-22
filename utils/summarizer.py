import json
import re
from utils.openai_client import get_openai_client

def extract_medical_summary(clinical_note: str) -> dict:
    client = get_openai_client()
    
    prompt = f"""You are a medical documentation assistant. Analyze the following clinical note and extract structured information.

Clinical Note:
{clinical_note}

Please provide a comprehensive analysis in the following JSON format:
{{
  "soap_note": {{
    "subjective": "Patient's reported symptoms and concerns",
    "objective": "Observable findings, measurements, test results",
    "assessment": "Clinical diagnosis and medical opinion",
    "plan": "Treatment plan and follow-up recommendations"
  }},
  "key_vitals": {{
    "blood_pressure": "e.g., 120/80 mmHg or N/A",
    "heart_rate": "e.g., 72 bpm or N/A",
    "temperature": "e.g., 98.6°F or N/A",
    "respiratory_rate": "e.g., 16 breaths/min or N/A",
    "oxygen_saturation": "e.g., 98% or N/A",
    "other": "Any other vitals mentioned"
  }},
  "exam_findings": [
    "List key physical examination findings",
    "Include both normal and abnormal findings",
    "Highlight any concerning findings"
  ],
  "key_information": {{
    "chief_complaint": "Primary reason for visit",
    "age": "Patient age if mentioned",
    "gender": "Patient gender if mentioned",
    "duration": "Duration of symptoms if mentioned"
  }}
}}

Extract all available information from the note. Use "N/A" or "Not mentioned" for missing data. Be thorough and accurate."""

    try:
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a medical documentation expert. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=8192
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        return {
            "error": f"Failed to process note: {str(e)}",
            "soap_note": {"subjective": "", "objective": "", "assessment": "", "plan": ""},
            "key_vitals": {},
            "exam_findings": [],
            "key_information": {}
        }

def format_soap_note(soap_data: dict) -> str:
    if not soap_data or "soap_note" not in soap_data:
        return "Error processing note"
    
    soap = soap_data["soap_note"]
    output = []
    
    output.append("**S (Subjective):**")
    output.append(soap.get("subjective", "N/A"))
    output.append("")
    
    output.append("**O (Objective):**")
    output.append(soap.get("objective", "N/A"))
    output.append("")
    
    output.append("**A (Assessment):**")
    output.append(soap.get("assessment", "N/A"))
    output.append("")
    
    output.append("**P (Plan):**")
    output.append(soap.get("plan", "N/A"))
    
    return "\n".join(output)

def format_vitals(vitals_data: dict) -> str:
    if not vitals_data:
        return "No vitals recorded"
    
    vitals = vitals_data.get("key_vitals", {})
    output = []
    
    vital_labels = {
        "blood_pressure": "Blood Pressure",
        "heart_rate": "Heart Rate",
        "temperature": "Temperature",
        "respiratory_rate": "Respiratory Rate",
        "oxygen_saturation": "O₂ Saturation",
        "other": "Other Vitals"
    }
    
    for key, label in vital_labels.items():
        value = vitals.get(key, "N/A")
        if value and value != "N/A":
            output.append(f"**{label}:** {value}")
    
    return "\n".join(output) if output else "No vitals recorded"

def format_exam_findings(exam_data: dict) -> str:
    if not exam_data or "exam_findings" not in exam_data:
        return "No exam findings recorded"
    
    findings = exam_data["exam_findings"]
    if not findings:
        return "No exam findings recorded"
    
    output = []
    for i, finding in enumerate(findings, 1):
        output.append(f"{i}. {finding}")
    
    return "\n".join(output)
