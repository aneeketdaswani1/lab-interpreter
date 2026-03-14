"""
Claude AI Explanation Module
Uses Claude API with streaming to generate biomarker explanations
"""
import os
from typing import List, Dict, Optional
from anthropic import Anthropic


def explain_biomarker(biomarker: Dict, studies: List[Dict] = None, client: Anthropic = None) -> str:
    """
    Generate a friendly explanation for a single biomarker result.
    
    Args:
        biomarker: Biomarker dict from parser with keys:
                   {name, value, unit, sex_specific_range, status, category, percent_from_range}
        studies: List of study dicts from researcher (optional)
        client: Anthropic client instance
        
    Returns:
        Full explanation string streamed from Claude
    """
    if client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)
    
    if studies is None:
        studies = []
    
    # Build context string
    name = biomarker.get("name", "Unknown")
    value = biomarker.get("value", "N/A")
    unit = biomarker.get("unit", "unknown")
    status = biomarker.get("status", "unknown")
    range_data = biomarker.get("sex_specific_range", [0, 100])
    percent_from_range = biomarker.get("percent_from_range", 0)
    
    range_str = f"{range_data[0]}-{range_data[1]}"
    
    # Get top 2 study abstracts
    study_context = ""
    if studies:
        study_context = "\n\nRecent Research:\n"
        for i, study in enumerate(studies[:2], 1):
            title = study.get("title", "Unknown")
            abstract = study.get("abstract_snippet", "No abstract")
            study_context += f"{i}. {title}\n   {abstract}\n"
    
    context = f"""Patient Lab Result:
- Biomarker: {name}
- Result: {value} {unit}
- Normal Range: {range_str}
- Status: {status}
- Position in Range: {percent_from_range}% (0% = low end, 100% = high end)
{study_context}"""
    
    system_prompt = """You are a friendly health educator explaining blood test results to a patient with no medical background. 
Be warm, clear, and reassuring but honest. Never diagnose. Always recommend consulting a doctor.
Structure your explanation as:
🔴/🟡/🟢 [STATUS IN PLAIN ENGLISH — 1 sentence what this means]
📖 What this measures: [1–2 sentences, simple analogy if helpful]  
⚠️ Why yours is [high/low]: [2–3 most common lifestyle causes]
🔬 What the research says: [1–2 sentences citing the studies provided]
✅ Good news: [1 sentence — what this level means practically, any silver linings]"""
    
    user_message = f"Please explain this blood test result:\n\n{context}"
    
    # Stream response
    explanation = ""
    
    try:
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        ) as stream:
            for text in stream.text_stream:
                explanation += text
    
    except Exception as e:
        explanation = f"Error generating explanation: {str(e)}"
    
    return explanation


def explain_all_flagged(biomarkers: List[Dict], research_dict: Dict[str, List[Dict]],
                       client: Anthropic = None) -> Dict[str, str]:
    """
    Generate explanations for all flagged (abnormal) biomarkers.
    
    Args:
        biomarkers: Full list of biomarker dicts from parser
        research_dict: Dict mapping biomarker names to study lists from researcher
        client: Anthropic client instance
        
    Returns:
        Dict mapping biomarker names to explanation strings
    """
    if client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)
    
    # Filter for flagged biomarkers (status != 'normal')
    flagged = [b for b in biomarkers if b.get('status') != 'normal']
    
    if not flagged:
        return {}
    
    explanations = {}
    
    print(f"\n📚 Generating explanations for {len(flagged)} biomarkers...")
    
    import streamlit as st
    progress_container = None
    progress_bar = None
    status_text = None
    
    try:
        # Try to use Streamlit if available
        progress_bar = st.progress(0)
        status_text = st.empty()
    except Exception:
        # Fallback to console if not in Streamlit context
        progress_bar = None
    
    for idx, biomarker in enumerate(flagged):
        name = biomarker.get("name", "Unknown")
        
        # Update progress
        if progress_bar:
            progress = (idx + 1) / len(flagged)
            progress_bar.progress(progress)
            status_text.text(f"📖 Explaining: {name}...")
        else:
            print(f"  • Explaining {name}... ({idx + 1}/{len(flagged)})", end=" ", flush=True)
        
        # Get studies for this biomarker
        studies = research_dict.get(name, [])
        
        # Generate explanation
        explanation = explain_biomarker(biomarker, studies, client)
        explanations[name] = explanation
        
        if not progress_bar:
            print("✓")
    
    # Clear progress indicators
    if progress_bar:
        progress_bar.empty()
        status_text.empty()
    
    print(f"✓ Generated {len(explanations)} explanations\n")
    
    return explanations
