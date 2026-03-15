"""
Biomarker Parsing Module
Parses extracted lab text to identify and standardize biomarker values
"""
import json
import re
import os
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher
import google.generativeai as genai


# Unit conversion constants
GLUCOSE_CONVERSION = 18.0182  # mg/dL to mmol/L
CHOLESTEROL_CONVERSION = 0.02586  # mg/dL to mmol/L


def parse_biomarkers(raw_text: str, sex: str = "male") -> List[Dict]:
    """
    Parse biomarker values from raw lab text.
    
    Args:
        raw_text: Extracted and cleaned text from PDF or lab report
        sex: 'male' or 'female' for gender-specific reference ranges
        
    Returns:
        List of parsed biomarker dicts with status and analysis
    """
    sex = sex.lower()
    if sex not in ["male", "female"]:
        sex = "male"
    
    # Load reference ranges
    ref_path = os.path.join(os.path.dirname(__file__), "..", "data", "reference_ranges.json")
    try:
        with open(ref_path, 'r') as f:
            reference_ranges = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load reference ranges: {e}")
        reference_ranges = {}
    
    # Attempt regex-based extraction
    biomarkers = _extract_via_regex(raw_text, reference_ranges, sex)
    
    # If no biomarkers found via regex, try Gemini fallback
    if not biomarkers or len(biomarkers) < 3:
        try:
            gemini_biomarkers = fallback_gemini_extraction(raw_text, reference_ranges, sex)
            if gemini_biomarkers:
                biomarkers.extend(gemini_biomarkers)
        except Exception as e:
            print(f"Gemini fallback extraction failed: {e}")
    
    return biomarkers


def _extract_via_regex(raw_text: str, reference_ranges: Dict, sex: str) -> List[Dict]:
    """
    Extract biomarkers using regex patterns.
    
    Matches patterns like:
    - 'HbA1c: 6.4%'
    - 'Glucose 5.2 mmol/L'
    - 'TSH   3.8   mIU/L  (0.4-4.0)'
    - 'Hemoglobin: 14.5 g/dL (13.5-17.5)'
    """
    biomarkers = []
    
    # Create regex pattern for common biomarker + value patterns
    # This pattern matches: [name] [optional: colon/equals] [optional spaces] [value] [optional spaces] [unit]
    
    # Build alternative names for biomarkers (includes common abbreviations)
    biomarker_aliases = _build_biomarker_aliases(reference_ranges)
    
    # Pattern to match biomarker lines
    # Matches lines with: name (colon|=|space+) number (unit) (optional reference range)
    lines = raw_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
        
        # Try to match each known biomarker
        for ref_name, ref_data in reference_ranges.items():
            aliases = biomarker_aliases.get(ref_name, [ref_name])
            
            for alias in aliases:
                # Build pattern: alias name followed by value and optional unit
                # Allow for flexible spacing and formatting
                pattern = (
                    rf'\b{re.escape(alias)}\b'  # Exact word boundary match
                    r'(?:\s*[:=]?\s*)?'  # Optional separator
                    r'(\d+\.?\d*)'  # Value (integer or decimal)
                    r'(?:\s*'  # Optional unit group
                    r'([a-zA-Z/%\-°]+|mIU/L|µmol|mmol/L|mg/dL|ng/mL|pg/mL|x10\^[0-9]/?[a-zA-Z]*)'  # Unit pattern
                    r')?'  # Unit is optional
                    r')?'  # Close optional unit group
                )
                
                match = re.search(pattern, line, re.IGNORECASE)
                
                if match:
                    try:
                        value = float(match.group(1))
                        unit = match.group(2) if len(match.groups()) > 1 and match.group(2) else None
                        
                        # Parse the biomarker
                        biomarker = _create_biomarker_dict(
                            ref_name, value, unit, ref_data, sex
                        )
                        
                        # Check if we already have this biomarker
                        if not any(b['name'] == biomarker['name'] for b in biomarkers):
                            biomarkers.append(biomarker)
                        
                        break  # Found a match, move to next line
                    
                    except (ValueError, IndexError):
                        continue
    
    return biomarkers


def _build_biomarker_aliases(reference_ranges: Dict) -> Dict[str, List[str]]:
    """
    Build common aliases/abbreviations for biomarkers.
    """
    aliases = {
        "HbA1c": ["HbA1c", "HbA1C", "hemoglobin A1c", "A1C"],
        "Glucose": ["Glucose", "glucose", "fasting glucose", "FBS"],
        "Total Cholesterol": ["Total Cholesterol", "total cholesterol", "cholesterol"],
        "LDL": ["LDL", "LDL-C", "ldl cholesterol"],
        "HDL": ["HDL", "HDL-C", "hdl cholesterol"],
        "Triglycerides": ["Triglycerides", "triglycerides", "TG"],
        "TSH": ["TSH", "tsh"],
        "T3": ["T3", "free T3", "freeT3", "T3 free"],
        "T4": ["T4", "free T4", "freeT4", "T4 free", "thyroxine"],
        "Vitamin D": ["Vitamin D", "vitamin d", "vitd", "D25OH"],
        "Vitamin B12": ["Vitamin B12", "B12", "cobalamin"],
        "Iron": ["Iron", "serum iron", "iron"],
        "Ferritin": ["Ferritin", "ferritin"],
        "Hemoglobin": ["Hemoglobin", "Hb", "haemoglobin"],
        "WBC": ["WBC", "white blood cells", "whiteblood cells"],
        "RBC": ["RBC", "red blood cells", "redblood cells"],
        "Platelets": ["Platelets", "PLT"],
        "ALT": ["ALT", "SGPT"],
        "AST": ["AST", "SGOT"],
        "Creatinine": ["Creatinine", "creatinine"],
        "eGFR": ["eGFR", "egfr"],
        "Sodium": ["Sodium", "Na"],
        "Potassium": ["Potassium", "K"],
        "Calcium": ["Calcium", "Ca"],
        "Magnesium": ["Magnesium", "Mg"],
        "CRP": ["CRP", "C-reactive protein"],
        "Testosterone": ["Testosterone"],
        "Estrogen": ["Estrogen", "estradiol"],
        "Cortisol": ["Cortisol"],
        "Insulin": ["Insulin", "fasting insulin"],
        "Uric Acid": ["Uric Acid", "uric acid"],
    }
    
    # Add auto-generated aliases from reference range names
    for key in reference_ranges.keys():
        if key not in aliases:
            aliases[key] = [key]
    
    return aliases


def _create_biomarker_dict(name: str, value: float, unit: Optional[str],
                          ref_data: Dict, sex: str) -> Dict:
    """
    Create a standardized biomarker dictionary with status analysis.
    """
    sex_key = f"{sex}_range"
    range_data = ref_data.get(sex_key, ref_data.get("male_range", [0, 100]))
    
    # Ensure range_data is a list of 2 numbers
    if not isinstance(range_data, (list, tuple)) or len(range_data) < 2:
        range_data = [0, 1000]
    
    min_val, max_val = float(range_data[0]), float(range_data[1])
    
    # Calculate percent from range
    if min_val == max_val:
        percent_from_range = 0.0
    else:
        percent_from_range = ((value - min_val) / (max_val - min_val)) * 100
    
    # Determine status
    status = _calculate_status(value, min_val, max_val)
    
    return {
        "name": name,
        "value": value,
        "unit": unit or ref_data.get("unit", "unknown"),
        "sex_specific_range": range_data,
        "status": status,
        "category": ref_data.get("category", "unknown"),
        "percent_from_range": round(percent_from_range, 1),
        "is_abnormal": status != "normal"
    }


def _calculate_status(value: float, min_val: float, max_val: float) -> str:
    """
    Calculate biomarker status with borderline detection.
    
    Borderline = within 10% of the range boundary
    """
    range_size = max_val - min_val
    tolerance = range_size * 0.10  # 10% tolerance
    
    if value < min_val:
        if value >= (min_val - tolerance):
            return "borderline_low"
        else:
            return "low"
    elif value > max_val:
        if value <= (max_val + tolerance):
            return "borderline_high"
        else:
            return "high"
    else:
        return "normal"


def fallback_gemini_extraction(raw_text: str,
                              reference_ranges: Dict, sex: str = "male") -> List[Dict]:
    """
    Fallback extraction using Google Gemini Flash.
    
    When regex extraction finds few/no biomarkers, send raw text to Gemini
    asking it to extract lab results as JSON.
    
    Args:
        raw_text: Raw lab report text
        reference_ranges: Reference ranges dictionary
        sex: Patient sex for range selection
        
    Returns:
        List of parsed biomarker dicts
    """
    sex = sex.lower()
    if sex not in ["male", "female"]:
        sex = "male"
    
    # Configure Gemini
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return []
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Create prompt for Gemini
    prompt = f"""You are an expert medical lab analyst. Extract ALL lab test results from this text.

Return ONLY a valid JSON array with NO OTHER TEXT. Each result should be an object with:
- name (string): exact biomarker name
- value (number): the numeric result
- unit (string): measurement unit (e.g., mg/dL, mIU/L, g/dL, ng/mL, etc.)

Example output:
[
  {{"name": "Glucose", "value": 105, "unit": "mg/dL"}},
  {{"name": "HbA1c", "value": 6.4, "unit": "%"}},
  {{"name": "Hemoglobin", "value": 14.5, "unit": "g/dL"}}
]

Lab Report Text:
{raw_text}"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Extract JSON from response (Gemini might add markdown code blocks)
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if not json_match:
            return []
        
        json_text = json_match.group(0)
        extracted_data = json.loads(json_text)
        
        if not isinstance(extracted_data, list):
            return []
        
        # Convert Gemini's output to biomarker dicts
        biomarkers = []
        for item in extracted_data:
            if not isinstance(item, dict) or 'name' not in item or 'value' not in item:
                continue
            
            name = item.get('name', '')
            
            # Fuzzy match against reference ranges
            matched_name = _fuzzy_match_biomarker(name, reference_ranges.keys())
            
            if matched_name and matched_name in reference_ranges:
                ref_data = reference_ranges[matched_name]
                value = float(item.get('value', 0))
                unit = item.get('unit', ref_data.get('unit', 'unknown'))
                
                biomarker = _create_biomarker_dict(
                    matched_name, value, unit, ref_data, sex
                )
                biomarkers.append(biomarker)
        
        return biomarkers
    
    except json.JSONDecodeError:
        print("Failed to parse Gemini's JSON response")
        return []
    except Exception as e:
        print(f"Gemini extraction error: {e}")
        return []


def _fuzzy_match_biomarker(query: str, candidates: List[str], threshold: float = 0.6) -> Optional[str]:
    """
    Fuzzy match biomarker name against candidates.
    
    Args:
        query: Biomarker name to match
        candidates: List of reference biomarker names
        threshold: Minimum similarity score (0-1)
        
    Returns:
        Best matching biomarker name or None
    """
    if not query:
        return None
    
    query_lower = query.lower().strip()
    best_match = None
    best_score = threshold
    
    for candidate in candidates:
        candidate_lower = candidate.lower().strip()
        
        # Exact match first
        if query_lower == candidate_lower:
            return candidate
        
        # Fuzzy match
        score = SequenceMatcher(None, query_lower, candidate_lower).ratio()
        
        if score > best_score:
            best_score = score
            best_match = candidate
    
    return best_match

