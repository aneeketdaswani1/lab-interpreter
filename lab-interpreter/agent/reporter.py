"""
PDF Report Builder Module
Generates comprehensive PDF health reports
"""
from fpdf import FPDF
from datetime import datetime
from typing import List, Dict


class ReportBuilder:
    """Build comprehensive PDF health reports"""
    
    def __init__(self, output_path: str = "health_report.pdf"):
        """Initialize report builder"""
        self.pdf = FPDF()
        self.output_path = output_path
    
    def create_report(self, 
                     patient_info: Dict,
                     biomarkers: List[Dict],
                     insights: str,
                     action_plan: Dict) -> str:
        """Create comprehensive health report"""
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        
        # Title
        self.pdf.cell(0, 10, "Lab Interpreter - Health Report", ln=True, align="C")
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
        
        # Patient Info
        self.pdf.ln(5)
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Patient Information", ln=True)
        self.pdf.set_font("Arial", "", 10)
        for key, value in patient_info.items():
            self.pdf.cell(0, 5, f"{key}: {value}", ln=True)
        
        # Biomarker Results
        self.pdf.ln(5)
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Biomarker Results", ln=True)
        self.pdf.set_font("Arial", "", 9)
        
        for biomarker in biomarkers[:15]:  # First 15 for space
            status_symbol = "✓" if biomarker.get("status") == "normal" else "!"
            self.pdf.cell(0, 5, 
                         f"{status_symbol} {biomarker.get('name')}: {biomarker.get('value')} {biomarker.get('unit', '')}",
                         ln=True)
        
        # Health Insights
        self.pdf.ln(5)
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, "Health Insights", ln=True)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.multi_cell(0, 4, insights[:500] + "...")  # Truncate for space
        
        # Save PDF
        self.pdf.output(self.output_path)
        return self.output_path
