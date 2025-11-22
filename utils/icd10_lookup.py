import csv
from difflib import SequenceMatcher
from typing import List, Dict, Optional

ICD10_DATA = []

def load_icd10_codes():
    """Load ICD-10 codes from CSV file into memory."""
    global ICD10_DATA
    
    if ICD10_DATA:
        return
    
    try:
        with open('attached_assets/ICD10codes_1763801327146.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4:
                    code = row[2].strip()
                    description = row[3].strip()
                    if code and description:
                        ICD10_DATA.append({
                            'code': code,
                            'description': description.lower()
                        })
    except Exception as e:
        print(f"Warning: Could not load ICD-10 codes: {e}")

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def find_icd10_code(diagnosis_text: str, threshold: float = 0.6) -> Optional[Dict[str, str]]:
    """
    Find the best matching ICD-10 code for a given diagnosis text.
    
    Args:
        diagnosis_text: The diagnosis text to match
        threshold: Minimum similarity score (0-1) to consider a match
    
    Returns:
        Dictionary with 'code' and 'text' keys, or None if no match found
    """
    if not ICD10_DATA:
        load_icd10_codes()
    
    if not ICD10_DATA or not diagnosis_text:
        return None
    
    diagnosis_lower = diagnosis_text.lower().strip()
    
    # First try exact match
    for entry in ICD10_DATA:
        if entry['description'] == diagnosis_lower:
            return {
                'code': entry['code'],
                'text': diagnosis_text
            }
    
    # Find best fuzzy match
    best_match = None
    best_score = threshold
    
    for entry in ICD10_DATA:
        # Check if key terms from diagnosis appear in description
        score = calculate_similarity(diagnosis_lower, entry['description'])
        
        if score > best_score:
            best_score = score
            best_match = entry
    
    if best_match:
        return {
            'code': best_match['code'],
            'text': diagnosis_text
        }
    
    return None

def search_icd10_codes(query: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    Search for ICD-10 codes matching a query.
    
    Args:
        query: Search query text
        limit: Maximum number of results to return
    
    Returns:
        List of dictionaries with 'code' and 'description' keys
    """
    if not ICD10_DATA:
        load_icd10_codes()
    
    if not query:
        return []
    
    query_lower = query.lower().strip()
    results = []
    
    for entry in ICD10_DATA:
        if query_lower in entry['description']:
            results.append({
                'code': entry['code'],
                'description': entry['description'].title()
            })
            if len(results) >= limit:
                break
    
    return results
