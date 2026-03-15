#!/usr/bin/env python3
"""
Generate a realistic sample lab report PDF for testing.
This creates a fake lab report from "MedLab Diagnostics" with 8 mixed biomarkers.
"""
from fpdf import FPDF
from datetime import datetime


def create_sample_lab_report():
    """Generate a realistic lab report PDF with mixed results."""
    
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Header
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "MedLab Diagnostics", ln=True)
    
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 4, "123 Health Street, Medical City, MC 12345", ln=True)
    pdf.cell(0, 4, "Phone: (555) 123-4567 | www.medlab.example.com", ln=True)
    
    pdf.ln(5)
    
    # Patient Info Box
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(50, 6, "PATIENT INFORMATION:")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "", ln=True)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(30, 5, "Name:")
    pdf.cell(50, 5, "John Smith", ln=True)
    
    pdf.cell(30, 5, "DOB:")
    pdf.cell(50, 5, "05/15/1975 (Age: 48)", ln=True)
    
    pdf.cell(30, 5, "Sex:")
    pdf.cell(50, 5, "Male", ln=True)
    
    pdf.cell(30, 5, "Specimen:")
    pdf.cell(50, 5, "Blood (Serum)", ln=True)
    
    pdf.cell(30, 5, "Collection:")
    pdf.cell(50, 5, "11/20/2024 14:30", ln=True)
    
    pdf.cell(30, 5, "Report Date:")
    pdf.cell(50, 5, f"{datetime.now().strftime('%m/%d/%Y')}", ln=True)
    
    pdf.ln(3)
    
    # Results Table
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, "LABORATORY RESULTS:", ln=True)
    
    pdf.ln(2)
    
    # Table header
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(200, 200, 200)
    
    col_widths = [45, 18, 20, 27, 30, 20]
    headers = ["Test Name", "Result", "Unit", "Reference Range", "Status", "Flag"]
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 6, header, border=1, fill=True, align="C")
    pdf.ln()
    
    # Sample data with mixed results
    results = [
        ("Glucose", "98", "mg/dL", "70-100", "[OK] Normal", ""),
        ("HbA1c", "6.1", "%", "4.0-5.6", "[HI] High", "ABNORMAL"),
        ("Total Cholesterol", "215", "mg/dL", "<200", "[HI] High", "ABNORMAL"),
        ("HDL Cholesterol", "62", "mg/dL", ">40", "[OK] Normal", ""),
        ("LDL Cholesterol", "142", "mg/dL", "<130", "[HI] High", "ABNORMAL"),
        ("Triglycerides", "128", "mg/dL", "<150", "[OK] Normal", ""),
        ("Vitamin D (25-OH)", "21", "ng/mL", "30-100", "[LO] Low", "ABNORMAL"),
        ("TSH", "4.8", "mIU/L", "0.4-4.0", "[HI] High", "ABNORMAL"),
    ]
    
    pdf.set_font("Helvetica", "", 8)
    
    for test_name, result, unit, ref_range, status, flag in results:
        pdf.cell(col_widths[0], 6, test_name, border=1, align="L")
        pdf.cell(col_widths[1], 6, result, border=1, align="R")
        pdf.cell(col_widths[2], 6, unit, border=1, align="C")
        pdf.cell(col_widths[3], 6, ref_range, border=1, align="C")
        pdf.cell(col_widths[4], 6, status, border=1, align="C")
        
        # Flag column - highlight if abnormal
        if flag:
            pdf.set_fill_color(255, 200, 200)
            pdf.cell(col_widths[5], 6, flag, border=1, fill=True, align="C")
            pdf.set_fill_color(255, 255, 255)
        else:
            pdf.cell(col_widths[5], 6, flag, border=1, align="C")
        
        pdf.ln()
    
    pdf.ln(5)
    
    # Notes section
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 6, "NOTES:", ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.multi_cell(0, 4, 
        "- Results are provided for informational purposes only.\n"
        "- Consult with your healthcare provider for interpretation and next steps.\n"
        "- Reference ranges may vary by laboratory.\n"
        "- Specimen collected after 12-hour fasting as requested.\n"
        "- Test performed and validated by certified medical technologists.")
    
    pdf.ln(3)
    
    # Footer
    pdf.set_font("Helvetica", "I", 7)
    pdf.cell(0, 4, "Report ID: ML-2024-001234 | Authorized by: Dr. Sarah Johnson, MD", ln=True)
    pdf.cell(0, 4, 
        "This report is confidential and intended only for the named patient and their healthcare provider.",
        ln=True)
    
    # Save to file
    pdf.output("/Users/aniketdaswani/Desktop/untitled folder 2/lab-interpreter/data/sample_results.pdf")
    print("✓ Sample PDF created: data/sample_results.pdf")


if __name__ == "__main__":
    create_sample_lab_report()
