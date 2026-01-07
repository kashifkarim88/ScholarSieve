import streamlit as st
import os
import json
from engine import ResearchInsightEngine

# 1. Page Config
st.set_page_config(
    page_title="ScholarSieve", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Styling
def inject_custom_css():
    st.markdown("""
        <style>
        /* Main background and font */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Title styling */
        .main-title {
            font-family: 'Inter', sans-serif;
            color: #1E1E1E;
            font-weight: 800;
            font-size: 3rem;
            margin-bottom: 0px;
        }
        
        /* Subtitle styling */
        .sub-title {
            color: #5E6AD2;
            font-weight: 400;
            font-size: 1.2rem;
            margin-top: -10px;
            margin-bottom: 30px;
        }

        /* Card-like expanders */
        .streamlit-expanderHeader {
            background-color: white !important;
            border-radius: 10px !important;
            border: 1px solid #E0E0E0 !important;
            font-weight: 600 !important;
            color: #1E1E1E !important;
        }
        
        /* Insight text styling */
        .insight-text {
            background-color: #ffffff;
            padding: 15px;
            border-left: 5px solid #5E6AD2;
            border-radius: 5px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #f0f2f6;
            border-right: 1px solid #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 3. Header Section
st.markdown('<p class="main-title">ScholarSieve</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Classical NLP Research Insight Engine</p>', unsafe_allow_html=True)

# 4. Helper Functions
def convert_to_markdown(data):
    md = f"# Research Insights: {data['title']}\n\n"
    headers = {
        "contribution": "Key Contributions",
        "methodology": "Methodology & Approach",
        "results": "Key Results & Findings",
        "limitations": "Limitations & Future Work"
    }
    for key, header in headers.items():
        if key in data and data[key]:
            md += f"## {header}\n"
            for insight in data[key]:
                md += f"- {insight}\n"
            md += "\n"
    return md

# 5. Sidebar logic
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2436/2436633.png", width=80) # Generic book/search icon
    st.header("Upload Control")
    uploaded_file = st.file_uploader("Drop your PDF here", type="pdf")
    st.divider()
    st.markdown("### 🛠 Tech Stack")
    st.caption("• PyMuPDF (Extraction)")
    st.caption("• Scikit-Learn (TF-IDF)")
    st.caption("• SpaCy (POS Tagging)")
    st.caption("• 100% Offline")

# 6. Main App Logic
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    with st.spinner("Sifting through sentences..."):
        try:
            engine = ResearchInsightEngine("temp.pdf")
            results = engine.get_insights(top_n=3)
            
            # --- Results UI ---
            col1, col2 = st.columns([2.5, 1], gap="large")
            
            with col1:
                st.subheader(f"📄 {results['title']}")
                
                # Custom styled display
                sections = {
                    "contribution": "🚀 Contributions",
                    "methodology": "🧪 Methodology",
                    "results": "📊 Results",
                    "limitations": "⚠️ Limitations"
                }

                for key, label in sections.items():
                    with st.expander(label, expanded=True):
                        if results[key]:
                            for item in results[key]:
                                # Use custom HTML class for the "insight card" look
                                st.markdown(f'<div class="insight-text">{item}</div>', unsafe_allow_html=True)
                        else:
                            st.info("No clear signals detected for this section.")

            with col2:
                st.markdown("### 📥 Actions")
                md_output = convert_to_markdown(results)
                
                st.download_button(
                    label="Download Markdown",
                    data=md_output,
                    file_name=f"{results['title']}_summary.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
                
                if st.button("Clear Cache"):
                    st.rerun()

                st.divider()
                st.markdown("### ⚙️ Statistics")
                st.metric(label="Insights Found", value=sum(len(v) for k, v in results.items() if isinstance(v, list)))

        except Exception as e:
            st.error(f"Analysis failed: {e}")
        finally:
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")
else:
    # Landing state
    st.empty()
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.info("Please upload a research paper in the sidebar to begin.")