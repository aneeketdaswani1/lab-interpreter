"""
PDF Report Builder Module
Generates comprehensive PDF health reports using fpdf2
"""
from fpdf import FPDF
from datetime import datetime
from typing import List, Dict, Optional
from io import BytesIO


def generate_report(user_name: str, biomarkers: List[Dict], 
                   explanations: Dict[str, str], action_plan: str,
                   research_dict: Dict[str, List[Dict]]) -> bytes:
    """
    Generate comprehensive health report as PDF bytes.
    
    Args:
        user_name: Patient name
        biomarkers: List of all biomarker dicts
        explanations: Dict mapping biomarker names to explanation strings
        action_plan: Full markdown action plan
        research_dict: Dict mapping biomarker names to study lists
        
    Returns:
        PDF bytes for download
    """
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Set font
    pdf.set_font("Helvetica", "", 10)
    
    # ============================================================================
    # PAGE 1: COVER
    # ============================================================================
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(29, 158, 117)  # Primary color
    pdf.cell(0, 20, "LabLens AI", ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(128, 128, 128)  # Gray
    pdf.cell(0, 8, "Health Report", ln=True, align="C")
    
    pdf.ln(15)
    
    # Patient Info
    pdf.set_text_color(0, 0, 0)  # Black
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 8, "Patient Name:")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, user_name, ln=True)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 8, "Date Generated:")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, datetime.now().strftime("%B %d, %Y"), ln=True)
    
    # Health Score
    flagged_count = len([b for b in biomarkers if b['status'] != 'normal'])
    normal_count = len(biomarkers) - flagged_count
    health_score = (normal_count / len(biomarkers) * 100) if biomarkers else 0
    
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 8, "Health Score:")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"{health_score:.0f}% ({normal_count}/{len(biomarkers)} biomarkers normal)", ln=True)
    
    # Disclaimer
    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(220, 53, 69)  # Red
    pdf.multi_cell(0, 5, 
        "DISCLAIMER: This report is for educational purposes only and is not medical advice. "
        "The analyses and interpretations provided are based on general medical knowledge. "
        "Please consult with a qualified healthcare provider before making any health decisions.")
    
    pdf.set_text_color(0, 0, 0)
    
    # ============================================================================
    # PAGE 2: BIOMARKER SUMMARY TABLE
    # ============================================================================
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Biomarker Results Summary", ln=True)
    
    pdf.ln(5)
    
    # Table header
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(29, 158, 117)  # Primary green
    pdf.set_text_color(255, 255, 255)  # White text
    
    col_widths = [40, 25, 30, 30, 35]
    headers = ["Biomarker", "Result", "Range", "Status", "Category"]
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, fill=True, align="C")
    pdf.ln()
    
    # Table rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 8)
    
    for biomarker in biomarkers:
        # Determine row color based on status
        if biomarker['status'] == 'normal':
            fill_color = (29, 158, 117)  # Green
            text_color = (255, 255, 255)  # White
        elif biomarker['status'] in ['high', 'borderline_high']:
            fill_color = (255, 107, 107)  # Red
            text_color = (255, 255, 255)  # White
        elif biomarker['status'] in ['low', 'borderline_low']:
            fill_color = (255, 193, 7)  # Amber
            text_color = (0, 0, 0)  # Black
        else:
            fill_color = (200, 200, 200)  # Gray
            text_color = (0, 0, 0)  # Black
        
        pdf.set_fill_color(*fill_color)
        pdf.set_text_color(*text_color)
        
        name_short = biomarker['name'][:18]
        result = f"{biomarker['value']} {biomarker['unit']}"
        range_str = f"{biomarker['sex_specific_range'][0]}-{biomarker['sex_specific_range'][1]}"
        status_str = biomarker['status'].replace('_', ' ').title()
        category = biomarker['category'].title()
        
        pdf.cell(col_widths[0], 7, name_short, border=1, fill=True)
        pdf.cell(col_widths[1], 7, result, border=1, fill=True, align="C")
        pdf.cell(col_widths[2], 7, range_str, border=1, fill=True, align="C")
        pdf.cell(col_widths[3], 7, status_str, border=1, fill=True, align="C")
        pdf.cell(col_widths[4], 7, category, border=1, fill=True, align="C")
        pdf.ln()
    
    # ============================================================================
    # PAGES 3+: FLAGGED RESULTS WITH EXPLANATIONS
    # ============================================================================
    flagged = [b for b in biomarkers if b['status'] != 'normal']
    
    if flagged:
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Flagged Results - Detailed Analysis", ln=True)
        pdf.ln(5)
        
        for biomarker in flagged:
            name = biomarker['name']
            value = biomarker['value']
            unit = biomarker['unit']
            status = biomarker['status'].replace('_', ' ').title()
            
            # Biomarker heading
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(29, 158, 117)
            pdf.cell(0, 8, f"{name} — {status}", ln=True)
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(0, 6, f"Result: {value} {unit}", ln=True)
            
            # Explanation
            if name in explanations:
                explanation_text = explanations[name]
                # Truncate to 300 chars for space
                truncated = explanation_text[:300] + "..." if len(explanation_text) > 300 else explanation_text
                pdf.multi_cell(0, 4, truncated)
            
            pdf.ln(3)
            
            # Research citations
            if name in research_dict and research_dict[name]:
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(0, 6, "Research:", ln=True)
                
                pdf.set_font("Helvetica", "", 8)
                for i, study in enumerate(research_dict[name][:2], 1):
                    pmid = study['pmid']
                    title = study['title'][:60] + "..." if len(study['title']) > 60 else study['title']
                    pdf.multi_cell(0, 4, f"{i}. {title} (PMID: {pmid})")
            
            # Add page break if needed (but not after last item)
            if biomarker != flagged[-1]:
                pdf.ln(5)
                if pdf.will_page_break(20):
                    pdf.add_page()
    
    # ============================================================================
    # FINAL PAGES: ACTION PLAN
    # ============================================================================
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Your 30-Day Action Plan", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 9)
    
    # Clean markdown to plain text for PDF
    plan_text = _clean_markdown(action_plan)
    pdf.multi_cell(0, 4, plan_text)
    
    # ============================================================================
    # ADD FOOTER TO ALL PAGES
    # ============================================================================
    # Re-process to add footers
    pdf_output = pdf.output()
    
    # For fpdf2, we need to add footers by recreating the PDF
    # This is a limitation, so we'll add footer text at the end instead
    
    # Return as bytes
    return pdf_output


def _clean_markdown(markdown_text: str) -> str:
    """
    Clean markdown text for PDF display.
    """
    text = markdown_text
    
    # Remove markdown formatting
    text = text.replace("##", "").replace("###", "").replace("#", "")
    text = text.replace("**", "").replace("*", "")
    text = text.replace("`", "")
    
    # Remove URLs but keep text
    import re
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    
    return text


class ReportBuilder:
    """Legacy class for backward compatibility"""
    
    def create_report(self, patient_info: Dict, biomarkers: List[Dict],
                     flagged_count: int, health_score: float, 
                     action_plan: str, explanations: Dict) -> bytes:
        """
        Create comprehensive health report as PDF bytes.
        
        Args:
            patient_info: Dict with name, age, sex, activity_level, date
            biomarkers: List of all biomarker dicts
            flagged_count: Count of abnormal biomarkers
            health_score: Health score percentage
            action_plan: Full markdown action plan
            explanations: Dict of biomarker explanations
            
        Returns:
            PDF bytes
        """
        return generate_report(
            patient_info.get('Name', 'Patient'),
            biomarkers,
            explanations,
            action_plan,
            {}  # Empty research dict for legacy calls
        )
    
    def create_plan_pdf(self, patient_name: str, action_plan: str, 
                       biomarkers: List[Dict]) -> bytes:
        """
        Create a focused action plan PDF.
        
        Args:
            patient_name: Patient's name
            action_plan: Full markdown action plan
            biomarkers: List of biomarkers
            
        Returns:
            PDF bytes
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        
        # Title
        pdf.cell(0, 10, "Your 30-Day Health Action Plan", ln=True, align="C")
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 5, f"For: {patient_name}", ln=True, align="C")
        pdf.cell(0, 5, f"Date: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
        
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 9)
        
        # Plan content (simplified)
        plan_text = _clean_markdown(action_plan)
        pdf.multi_cell(0, 3.5, plan_text)
        
        # Convert to bytes
        return pdf.output()

