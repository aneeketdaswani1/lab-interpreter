"""
Lab Interpreter - Streamlit Application
AI-powered biomarker analysis and personalized health insights
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import os

from agent.extractor import extract_text_from_pdf
from agent.parser import parse_biomarkers
from agent.researcher import research_flagged_biomarkers
from agent.explainer import explain_all_flagged
from agent.planner import generate_action_plan
from agent.reporter import ReportBuilder


# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="LabLens AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS for dark theme enhancements
st.markdown("""
<style>
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #1D9E75;
        margin-bottom: 0.5em;
    }
    .tagline {
        font-size: 1.1em;
        color: #888;
        margin-bottom: 2em;
    }
    .disclaimer-box {
        padding: 1em;
        border-radius: 0.5em;
        background-color: rgba(220, 53, 69, 0.1);
        border-left: 4px solid #DC3545;
        color: #DC3545;
        font-weight: bold;
        margin: 1em 0;
    }
    .metric-card {
        padding: 1.5em;
        border-radius: 0.75em;
        background-color: #262730;
        border: 1px solid #404856;
        text-align: center;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25em 0.75em;
        border-radius: 999px;
        font-size: 0.85em;
        font-weight: bold;
    }
    .status-high { background-color: rgba(220, 53, 69, 0.2); color: #FF6B6B; }
    .status-low { background-color: rgba(255, 193, 7, 0.2); color: #FFC107; }
    .status-normal { background-color: rgba(29, 158, 117, 0.2); color: #1D9E75; }
    .status-borderline { background-color: rgba(255, 193, 7, 0.2); color: #FFC107; }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown('<div class="main-title">🧬 LabLens AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Understand your blood work</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # PDF Upload
    st.header("📄 Upload Lab Results")
    uploaded_pdf = st.file_uploader("Choose a PDF lab report", type="pdf")
    
    st.divider()
    
    # User Profile Form
    st.header("👤 Your Profile")
    
    first_name = st.text_input("First name", placeholder="e.g., Alex")
    age = st.slider("Age", 18, 90, 35)
    sex = st.radio("Sex", ["Male", "Female", "Prefer not to say"], horizontal=True)
    
    activity_level = st.selectbox(
        "Activity level",
        ["Sedentary", "Light", "Moderate", "Active"],
        help="How active are you on average?"
    )
    
    dietary_preference = st.selectbox(
        "Dietary preference",
        ["Omnivore", "Vegetarian", "Vegan", "Keto"],
    )
    
    health_goals = st.multiselect(
        "Health goals",
        ["Weight loss", "Energy", "Heart health", "Hormonal balance", "Athletic performance", "Longevity"],
        default=["Energy"]
    )
    
    st.divider()
    
    # Disclaimer
    st.markdown(
        '<div class="disclaimer-box">⚠️ For educational purposes only. Not medical advice. Always consult a healthcare provider.</div>',
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Analyse Button
    analyse_clicked = st.button("🔍 Analyse My Results", use_container_width=True, type="primary")


# ============================================================================
# MAIN AREA
# ============================================================================
if analyse_clicked:
    if not uploaded_pdf or not first_name:
        st.error("Please upload a PDF and enter your name to continue.")
        st.stop()
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Progress indicators
    progress_container = st.container()
    
    with progress_container:
        col1, col2 = st.columns([0.6, 0.4])
        
        with col1:
            st.subheader("📊 Analysis Progress")
        
        progress_steps = {
            "1": {"label": "Extracting text from PDF", "status": "⏳"},
            "2": {"label": "Parsing biomarkers", "status": "⏳"},
            "3": {"label": "Searching PubMed", "status": "⏳"},
            "4": {"label": "Generating explanations", "status": "⏳"},
            "5": {"label": "Building action plan", "status": "⏳"}
        }
        
        progress_placeholder = st.empty()
    
    try:
        # Step 1: Extract PDF
        with progress_placeholder.container():
            for step_id, step_data in progress_steps.items():
                if int(step_id) == 1:
                    st.write(f"✓ {step_data['label']}")
                else:
                    st.write(f"{step_data['status']} {step_data['label']}")
        
        pdf_bytes = uploaded_pdf.read()
        raw_text = extract_text_from_pdf(pdf_bytes)
        
        st.session_state.raw_text = raw_text
        
        # Step 2: Parse biomarkers
        with progress_placeholder.container():
            for step_id, step_data in progress_steps.items():
                if int(step_id) <= 2:
                    st.write(f"✓ {step_data['label']}")
                else:
                    st.write(f"{step_data['status']} {step_data['label']}")
        
        biomarkers = parse_biomarkers(raw_text, sex=sex.lower())
        
        if not biomarkers:
            st.error("Could not parse any biomarkers from the PDF. Please check the file format.")
            st.stop()
        
        st.session_state.biomarkers = biomarkers
        
        # Step 3: Research flagged biomarkers
        with progress_placeholder.container():
            for step_id, step_data in progress_steps.items():
                if int(step_id) <= 3:
                    st.write(f"✓ {step_data['label']}")
                else:
                    st.write(f"{step_data['status']} {step_data['label']}")
        
        research_dict = research_flagged_biomarkers(biomarkers)
        st.session_state.research_dict = research_dict
        
        # Step 4: Generate explanations
        with progress_placeholder.container():
            for step_id, step_data in progress_steps.items():
                if int(step_id) <= 4:
                    st.write(f"✓ {step_data['label']}")
                else:
                    st.write(f"{step_data['status']} {step_data['label']}")
        
        explanations = explain_all_flagged(biomarkers, research_dict)
        st.session_state.explanations = explanations
        
        # Step 5: Build action plan
        with progress_placeholder.container():
            st.write("✓ Extracting text from PDF")
            st.write("✓ Parsing biomarkers")
            st.write("✓ Searching PubMed")
            st.write("✓ Generating explanations")
            st.write("✓ Building action plan")
        
        user_profile = {
            "name": first_name,
            "age": age,
            "sex": sex.lower(),
            "activity_level": activity_level.lower(),
            "dietary_preference": dietary_preference.lower(),
            "health_goals": health_goals
        }
        
        action_plan = generate_action_plan(biomarkers, user_profile, research_dict)
        st.session_state.action_plan = action_plan
        st.session_state.user_profile = user_profile
        
        st.session_state.analysis_complete = True
        
        # Clear progress container
        progress_placeholder.empty()
        st.success("✅ Analysis complete!")
        st.balloons()
    
    except Exception as e:
        st.error(f"Error during analysis: {str(e)}")
        st.stop()


# ============================================================================
# DISPLAY RESULTS (if analysis complete)
# ============================================================================
if st.session_state.get('analysis_complete', False):
    biomarkers = st.session_state.biomarkers
    research_dict = st.session_state.research_dict
    explanations = st.session_state.explanations
    action_plan = st.session_state.action_plan
    user_profile = st.session_state.user_profile
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Overview", "🧪 Biomarker Details", "🔬 Research", "📋 Action Plan", "📑 Report"]
    )
    
    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    with tab1:
        st.header("Your Health Overview")
        
        # Health Score Card
        flagged = [b for b in biomarkers if b['status'] != 'normal']
        normal_count = len(biomarkers) - len(flagged)
        total_count = len(biomarkers)
        health_percentage = (normal_count / total_count) * 100 if total_count > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Health Score",
                f"{health_percentage:.0f}%",
                delta=f"{normal_count}/{total_count} Normal"
            )
        
        with col2:
            high_count = len([b for b in flagged if b['status'] in ['high', 'borderline_high']])
            st.metric("🔴 Flagged High", high_count, delta="needs attention")
        
        with col3:
            low_count = len([b for b in flagged if b['status'] in ['low', 'borderline_low']])
            st.metric("🟡 Flagged Low", low_count, delta="needs attention")
        
        with col4:
            st.metric("🟢 Normal Range", normal_count, delta=f"{health_percentage:.0f}% optimal")
        
        st.divider()
        
        # Horizontal Bar Chart - Biomarkers as % of range
        st.subheader("Biomarker Position in Normal Range")
        
        chart_data = []
        for b in biomarkers:
            status = b['status']
            if status == 'normal':
                color = '#1D9E75'  # Green
            elif status in ['high', 'borderline_high']:
                color = '#FF6B6B'  # Red
            else:
                color = '#FFC107'  # Amber
            
            chart_data.append({
                'name': b['name'],
                'percent': min(max(b['percent_from_range'], 0), 100),
                'value': b['value'],
                'unit': b['unit'],
                'status': status,
                'color': color
            })
        
        df_chart = pd.DataFrame(chart_data)
        
        fig_bar = go.Figure()
        for idx, row in df_chart.iterrows():
            fig_bar.add_trace(go.Bar(
                y=[row['name']],
                x=[row['percent']],
                orientation='h',
                marker=dict(color=row['color']),
                text=f"{row['percent']:.0f}% ({row['value']} {row['unit']})",
                textposition='outside',
                hovertemplate=f"<b>{row['name']}</b><br>Value: {row['value']} {row['unit']}<br>% from range: {row['percent']:.1f}%<extra></extra>",
                showlegend=False
            ))
        
        fig_bar.update_layout(
            xaxis_title="Position in Normal Range (%)",
            yaxis_title="",
            height=max(400, len(df_chart) * 25),
            margin=dict(l=150, r=100),
            xaxis=dict(range=[0, 100]),
            showlegend=False,
            hovermode='closest'
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.divider()
        
        # Category Breakdown - Radar Chart
        st.subheader("Health by Category")
        
        categories = {
            'Metabolic': [],
            'Lipids': [],
            'Thyroid': [],
            'Hormones': [],
            'Vitamins': [],
            'Inflammation': []
        }
        
        for b in biomarkers:
            cat = b.get('category', '').capitalize()
            if cat in categories:
                is_normal = 1 if b['status'] == 'normal' else 0
                categories[cat].append(is_normal)
        
        # Calculate % optimal per category
        category_scores = []
        for cat, values in categories.items():
            if values:
                score = (sum(values) / len(values)) * 100
                category_scores.append(score)
            else:
                category_scores.append(0)
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=category_scores,
            theta=list(categories.keys()),
            fill='toself',
            name='% Optimal',
            line=dict(color='#1D9E75'),
            fillcolor='rgba(29, 158, 117, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # ========================================================================
    # TAB 2: BIOMARKER DETAILS
    # ========================================================================
    with tab2:
        st.header("Detailed Biomarker Analysis")
        
        # Flagged biomarkers
        flagged = [b for b in biomarkers if b['status'] != 'normal']
        
        if flagged:
            st.subheader("🚨 Flagged Biomarkers")
            
            for biomarker in flagged:
                with st.expander(f"**{biomarker['name']}** — {biomarker['status'].upper()}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Your Result", f"{biomarker['value']} {biomarker['unit']}")
                    
                    with col2:
                        range_data = biomarker['sex_specific_range']
                        st.metric("Normal Range", f"{range_data[0]}-{range_data[1]} {biomarker['unit']}")
                    
                    with col3:
                        status_emoji = {
                            'high': '🔴',
                            'borderline_high': '🟡',
                            'low': '🔴',
                            'borderline_low': '🟡'
                        }.get(biomarker['status'], '⚪')
                        st.metric("Status", f"{status_emoji} {biomarker['status'].replace('_', ' ').title()}")
                    
                    st.divider()
                    
                    # Explanation from Claude
                    if biomarker['name'] in explanations:
                        st.markdown(explanations[biomarker['name']])
        
        # Normal biomarkers (collapsed)
        normal = [b for b in biomarkers if b['status'] == 'normal']
        
        if normal:
            with st.expander(f"✅ Normal Biomarkers ({len(normal)})"):
                normal_df = pd.DataFrame([
                    {
                        'Biomarker': b['name'],
                        'Result': f"{b['value']} {b['unit']}",
                        'Range': f"{b['sex_specific_range'][0]}-{b['sex_specific_range'][1]}",
                        'Category': b['category']
                    }
                    for b in normal
                ])
                
                st.dataframe(normal_df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # TAB 3: RESEARCH
    # ========================================================================
    with tab3:
        st.header("PubMed Research")
        
        if not research_dict:
            st.info("No research studies found for your flagged biomarkers.")
        else:
            for biomarker_name, studies in research_dict.items():
                with st.expander(f"**{biomarker_name}** ({len(studies)} studies)"):
                    for study in studies:
                        st.subheader(study['title'])
                        
                        st.write(study['abstract_snippet'])
                        
                        col1, col2 = st.columns([0.8, 0.2]
                        )
                        
                        with col2:
                            st.link_button(
                                "📖 Read on PubMed",
                                study['pubmed_url'],
                                use_container_width=True
                            )
                        
                        st.divider()
    
    # ========================================================================
    # TAB 4: ACTION PLAN
    # ========================================================================
    with tab4:
        st.header("Your 30-Day Action Plan")
        
        st.markdown(action_plan)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.write("*Copy functionality requires browser support*")
                st.code(action_plan, language="markdown")
        
        with col2:
            if st.button("⬇️ Download as PDF", use_container_width=True):
                try:
                    report_builder = ReportBuilder()
                    pdf_bytes = report_builder.create_plan_pdf(
                        user_profile['name'],
                        action_plan,
                        biomarkers
                    )
                    
                    st.download_button(
                        "Download Plan PDF",
                        data=pdf_bytes,
                        file_name=f"health_plan_{user_profile['name'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {e}")
        
        with col3:
            if st.button("🔄 Share Plan", use_container_width=True):
                st.info("Share functionality coming soon!")
    
    # ========================================================================
    # TAB 5: REPORT
    # ========================================================================
    with tab5:
        st.header("Full Health Report")
        
        st.write("Generate a comprehensive PDF report with all your biomarker data, analysis, and recommendations.")
        
        st.divider()
        
        if st.button("⬇️ Download Full Report as PDF", use_container_width=True, type="primary"):
            try:
                report_builder = ReportBuilder()
                pdf_bytes = report_builder.create_report(
                    patient_info={
                        'Name': user_profile['name'],
                        'Age': user_profile['age'],
                        'Sex': user_profile['sex'].title(),
                        'Activity Level': user_profile['activity_level'].title(),
                        'Date': pd.Timestamp.now().strftime('%Y-%m-%d')
                    },
                    biomarkers=biomarkers,
                    flagged_count=len([b for b in biomarkers if b['status'] != 'normal']),
                    health_score=health_percentage,
                    action_plan=action_plan,
                    explanations=explanations
                )
                
                st.download_button(
                    "📥 Download Report",
                    data=pdf_bytes,
                    file_name=f"lab_report_{user_profile['name'].replace(' ', '_')}_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success("PDF ready for download!")
            
            except Exception as e:
                st.error(f"Error generating report: {e}")
else:
    # Welcome screen
    st.markdown("""
    # 🧬 Welcome to LabLens AI
    
    Understand your blood work with AI-powered analysis.
    
    ## How it works:
    
    1. **Upload** your lab report PDF
    2. **Profile** - Tell us about yourself
    3. **Analyze** - We extract, parse, and research your results
    4. **Interpret** - Get AI-powered explanations
    5. **Act** - Receive a personalized 30-day action plan
    
    ---
    
    ### Features:
    
    ✨ **AI Explanations** - Friendly, non-medical guides for each biomarker
    
    📊 **Visual Analytics** - See exactly where your values fall
    
    🔬 **PubMed Research** - Latest studies for your specific results
    
    📋 **Personalized Plans** - 30-day protocols tailored to your goals
    
    📑 **Professional Reports** - Download comprehensive PDFs
    
    ---
    
    **Get started** by uploading a PDF in the sidebar →
    """)
    
    st.info("👈 Use the sidebar to upload your lab results and get started!")

