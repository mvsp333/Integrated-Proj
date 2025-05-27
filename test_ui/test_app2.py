import streamlit as st
import time
from utils.add_custom_css import add_custom_css
from nlp.extract_pdf_text import extract_text_from_pdf
from nlp.extract_url_text import extract_text_from_url
from nlp.classify import classify_text as classify_text
from nlp.summarize import extractive_summarization
from nlp.extract_keywords import extract_keywords
from nltk.tokenize import sent_tokenize
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# Page Configuration
st.set_page_config(
    page_title="NewsAI Pro - Advanced Text Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply modern CSS styling
add_custom_css()

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Header Navigation
col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
with col1:
    st.markdown("<h2 style='color: #2c3e50; font-family: Inter;'>🧠 NewsAI Pro</h2>", unsafe_allow_html=True)
with col2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "home"
with col3:
    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.current_page = "analytics"
with col4:
    if st.button("🔍 Results", use_container_width=True):
        st.session_state.current_page = "results"

st.markdown("---")

# Home Page
if st.session_state.current_page == "home":
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">NewsAI Pro</h1>
        <p class="hero-subtitle">Advanced AI-Powered Text Analytics & News Intelligence</p>
        <p style="font-size: 1.1rem; opacity: 0.8;">Transform any text content into actionable insights with cutting-edge NLP technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Methods
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 2rem;'>Choose Your Input Method</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="input-method-card">
            <div style="text-align: center;">
                <span class="card-icon">📄</span>
                <h3 class="card-title">PDF Upload</h3>
                <p class="card-description">Upload and analyze PDF documents with advanced text extraction</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['pdf'], key="pdf_upload", label_visibility="collapsed")
        if st.button("Process PDF Document", key="pdf_btn", use_container_width=True):
            if uploaded_file:
                with st.spinner("🔄 Processing PDF document..."):
                    text_content = extract_text_from_pdf(uploaded_file)
                    if text_content:
                        st.session_state.current_text = text_content
                        st.success("✅ PDF processed successfully!")
                        time.sleep(1)
                        st.session_state.current_page = "analytics"
                        st.rerun()
            else:
                st.error("Please upload a PDF file first")
    
    with col2:
        st.markdown("""
        <div class="input-method-card">
            <div style="text-align: center;">
                <span class="card-icon">🌐</span>
                <h3 class="card-title">URL Analysis</h3>
                <p class="card-description">Fetch and analyze content directly from web articles</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        url_input = st.text_input("", placeholder="Enter article URL...", key="url_input", label_visibility="collapsed")
        if st.button("Analyze Web Content", key="url_btn", use_container_width=True):
            if url_input:
                with st.spinner("🔄 Fetching web content..."):
                    text_content = extract_text_from_url(url_input)
                    if text_content:
                        st.session_state.current_text = text_content
                        st.success("✅ Content fetched successfully!")
                        time.sleep(1)
                        st.session_state.current_page = "analytics"
                        st.rerun()
            else:
                st.error("Please enter a valid URL")
    
    with col3:
        st.markdown("""
        <div class="input-method-card">
            <div style="text-align: center;">
                <span class="card-icon">✍️</span>
                <h3 class="card-title">Direct Input</h3>
                <p class="card-description">Paste or type your text content for immediate analysis</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        text_input = st.text_area("", placeholder="Paste your text here...", height=100, key="text_input", label_visibility="collapsed")
        if st.button("Analyze Text Content", key="text_btn", use_container_width=True):
            if text_input:
                st.session_state.current_text = text_input
                st.success("✅ Text ready for analysis!")
                time.sleep(1)
                st.session_state.current_page = "analytics"
                st.rerun()
            else:
                st.error("Please enter some text content")

# Analytics Page
elif st.session_state.current_page == "analytics":
    if not st.session_state.current_text:
        st.warning("⚠️ No content available for analysis. Please go back to Home and input some content.")
        if st.button("← Back to Home"):
            st.session_state.current_page = "home"
            st.rerun()
    else:
        st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔄 Processing Content</h1>", unsafe_allow_html=True)
        
        # Progress bars for analysis steps
        progress_container = st.container()
        with progress_container:
            col1, col2 = st.columns([3, 1])
            with col1:
                progress_bar = st.progress(0)
                status_text = st.empty()
            
            # Step 1: Text Classification
            status_text.text("🤖 Classifying content...")
            progress_bar.progress(25)
            time.sleep(1)
            category = classify_text(st.session_state.current_text)
            
            # Step 2: Summarization
            status_text.text("📝 Generating summary...")
            progress_bar.progress(50)
            time.sleep(1)
            summary = extractive_summarization(st.session_state.current_text)
            
            # Step 3: Keyword Extraction
            status_text.text("🔑 Extracting keywords...")
            progress_bar.progress(75)
            time.sleep(1)
            keywords = extract_keywords(st.session_state.current_text)
            
            # Step 4: Complete
            status_text.text("✅ Analysis complete!")
            progress_bar.progress(100)
            time.sleep(1)
            
            st.session_state.analysis_data = {
                'text': st.session_state.current_text,
                'category': category,
                'summary': summary,
                'keywords': keywords
            }
            
            st.success("🎉 Analysis completed successfully!")
            time.sleep(1)
            st.session_state.current_page = "results"
            st.rerun()

# Results Page
elif st.session_state.current_page == "results":
    if not st.session_state.analysis_data:
        st.warning("⚠️ No analysis results available. Please analyze some content first.")
        if st.button("← Back to Home"):
            st.session_state.current_page = "home"
            st.rerun()
    else:
        results = st.session_state.analysis_data
        
        # Dashboard Header
        st.markdown("<h1 style='text-align: center; color: #2c3e50; margin-bottom: 2rem;'>📊 Analysis Dashboard</h1>", unsafe_allow_html=True)
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{results['category'].title()}</div>
                <div class="metric-label">Category</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            word_count = len(results['text'].split())
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{word_count:,}</div>
                <div class="metric-label">Words</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            sentence_count = len(sent_tokenize(results['text']))
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{sentence_count}</div>
                <div class="metric-label">Sentences</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            keyword_count = len(results['keywords']) if results['keywords'] else 0
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{keyword_count}</div>
                <div class="metric-label">Keywords</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Content Sections
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Summary Section
            st.markdown("""
            <div class="content-section">
                <h3 class="section-title">📝 AI-Generated Summary</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3d72b4;'>{results['summary']}</div>", unsafe_allow_html=True)
            
            # Original Text Section
            st.markdown("""
            <div class="content-section" style="margin-top: 2rem;">
                <h3 class="section-title">📄 Original Content</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📖 View Full Content", expanded=False):
                st.markdown(f"<div style='background: white; padding: 1rem; border-radius: 8px; max-height: 400px; overflow-y: auto;'>{results['text']}</div>", unsafe_allow_html=True)
        
        with col2:
            # Keywords Section
            st.markdown("""
            <div class="content-section">
                <h3 class="section-title">🔑 Key Terms</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if results['keywords']:
                keyword_html = ""
                for kw in results['keywords'][:15]:
                    keyword_html += f'<span class="keyword-tag">{kw}</span>'
                st.markdown(f"<div>{keyword_html}</div>", unsafe_allow_html=True)
            else:
                st.info("No keywords extracted from the content.")
            
            # Category Display
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class="content-section">
                <h3 class="section-title">🏷️ Content Category</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: center;"><span class="category-badge">{results["category"]}</span></div>', unsafe_allow_html=True)