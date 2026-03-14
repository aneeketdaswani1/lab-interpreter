"""
Lab Interpreter - Streamlit Application
Main entry point for the biomarker analysis platform
"""
import streamlit as st
from agent.extractor import PDFExtractor
from agent.parser import BiomarkerParser
from agent.researcher import PubMedResearcher
from agent.explainer import ClaudeExplainer
from agent.planner import ActionPlanner
from agent.reporter import ReportBuilder


def main():
    st.set_page_config(
        page_title="Lab Interpreter",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧪 Lab Interpreter")
    st.markdown("AI-powered biomarker analysis and personalized health insights")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select a page:",
            ["Upload Lab Results", "Analysis", "Research", "Action Plan", "Report"]
        )
    
    if page == "Upload Lab Results":
        st.header("📄 Upload Lab Results")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file:
            st.success("File uploaded successfully!")
    
    elif page == "Analysis":
        st.header("📊 Biomarker Analysis")
        st.info("Upload lab results first to analyze biomarkers")
    
    elif page == "Research":
        st.header("🔬 PubMed Research")
        st.info("Biomarker research information will appear here")
    
    elif page == "Action Plan":
        st.header("📋 30-Day Action Plan")
        st.info("Your personalized action plan will be generated here")
    
    elif page == "Report":
        st.header("📑 Health Report")
        st.info("Generate a comprehensive PDF report")


if __name__ == "__main__":
    main()
