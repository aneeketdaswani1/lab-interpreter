"""
PDF Text Extraction Module
Extracts text and structured data from lab result PDFs
"""
import fitz  # PyMuPDF
import re


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract all text from uploaded PDF bytes.
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        Cleaned text string with OCR artifacts removed
        
    Raises:
        ValueError: If PDF cannot be parsed
    """
    try:
        # Open PDF from bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        
        # Extract text from all pages
        for page in doc:
            page_text = page.get_text()
            text += page_text + "\n"
        
        doc.close()
        
        # Clean the extracted text
        cleaned_text = _clean_text(text)
        return cleaned_text
    
    except Exception as e:
        raise ValueError(f"Error extracting PDF text: {str(e)}")


def _clean_text(text: str) -> str:
    """
    Clean extracted text by removing OCR artifacts and excessive whitespace.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove form feed characters and other control characters
    text = re.sub(r'[\f\x00\x01\x02\x03\x04\x05\x06\x07\x08]', '', text)
    
    # Fix common OCR artifacts
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Replace multiple newlines with double newline (preserve structure)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix spaces around punctuation that OCR often messes up
    text = re.sub(r'\s+([.,;:])', r'\1', text)
    
    # Fix common OCR misreadings (e.g., 'l' instead of '1', 'O' instead of '0')
    # Only in numeric contexts - be careful not to break real text
    text = re.sub(r'(\D)([lI])([,\s])(\d+\.?\d*)', r'\1\4', text)
    
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text
