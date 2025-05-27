# Page Configuration - MUST BE FIRST
import streamlit as st

st.set_page_config(
    page_title="NewsAI Pro - Advanced Text Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Now import other modules
import time
from utils.add_custom_css import add_custom_css as add_modern_css
from nlp.extract_pdf_text import extract_text_from_pdf
from nlp.extract_url_text import extract_text_from_url
from nlp.classify import classify_text as classify_text
from nlp.summarize import extractive_summarization
from nlp.extract_keywords import extract_keywords
from nltk.tokenize import sent_tokenize
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Apply modern CSS styling
add_modern_css()

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Header Navigation
# col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

col1, col2, col3= st.columns([3, 1, 1])
with col1:
    st.markdown("<h2 style='color: #2c3e50; font-family: Inter;'>🧠 NewsAI Pro</h2>", unsafe_allow_html=True)
with col2:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "home"
with col3:
    if st.button("📊 Analytics", use_container_width=True):
        st.session_state.current_page = "analytics"
# with col4:
#     if st.button("🔍 Results", use_container_width=True):
#         st.session_state.current_page = "results"

st.markdown("---")

# Home Page
if st.session_state.current_page == "home":
    # Dynamic Welcome Banner
    st.markdown("""
    <div style="background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%); 
                padding: 4rem 2rem; border-radius: 25px; text-align: center; margin-bottom: 3rem;
                position: relative; overflow: hidden;">
        <div style="position: absolute; top: 10%; left: 10%; width: 20px; height: 20px; 
                    background: rgba(255,255,255,0.3); border-radius: 50%; animation: pulse 2s infinite;"></div>
        <div style="position: absolute; top: 70%; right: 15%; width: 15px; height: 15px; 
                    background: rgba(255,255,255,0.4); border-radius: 50%; animation: pulse 3s infinite;"></div>
        <h1 style="font-size: 4rem; font-weight: 800; color: #2c3e50; margin-bottom: 1rem; 
                   text-shadow: 2px 2px 8px rgba(0,0,0,0.1);">🚀 TextMind AI</h1>
        <p style="font-size: 1.5rem; color: #34495e; font-weight: 300; margin-bottom: 2rem;">
            Unlock the Power of Intelligent Text Analysis
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.8); padding: 1rem 2rem; border-radius: 50px; backdrop-filter: blur(10px);">
                <span style="font-weight: 600; color: #2c3e50;">🎯 Smart Classification</span>
            </div>
            <div style="background: rgba(255,255,255,0.8); padding: 1rem 2rem; border-radius: 50px; backdrop-filter: blur(10px);">
                <span style="font-weight: 600; color: #2c3e50;">⚡ Instant Summaries</span>
            </div>
            <div style="background: rgba(255,255,255,0.8); padding: 1rem 2rem; border-radius: 50px; backdrop-filter: blur(10px);">
                <span style="font-weight: 600; color: #2c3e50;">🔍 Key Insights</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Input Sections
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 style="color: #2c3e50; font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
            How Would You Like to Begin?
        </h2>
        <p style="color: #7f8c8d; font-size: 1.2rem;">Choose your preferred input method and start analyzing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabbed Interface
    tab1, tab2, tab3 = st.tabs(["📄 **Upload Document**", "🌐 **Web Article**", "✍️ **Direct Text**"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 3rem; border-radius: 20px; text-align: center; margin: 2rem 0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
                <h3 style="color: white; font-size: 1.8rem; margin-bottom: 1rem;">PDF Document Analysis</h3>
                <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-bottom: 2rem;">
                    Extract and analyze text from your PDF documents with advanced OCR technology
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choose a PDF file", 
                type=['pdf'], 
                key="pdf_upload",
                help="Upload PDF files up to 200MB"
            )
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("🚀 **Analyze PDF**", key="pdf_btn", use_container_width=True, type="primary"):
                    if uploaded_file:
                        with st.spinner("🔄 Extracting text from PDF..."):
                            progress = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                progress.progress(i + 1)
                            text_content = extract_text_from_pdf(uploaded_file)
                            if text_content:
                                st.session_state.current_text = text_content
                                st.success("✅ PDF processed successfully!")
                                # st.balloons()
                                time.sleep(2)
                                st.session_state.current_page = "analytics"
                                st.rerun()
                    else:
                        st.error("⚠️ Please upload a PDF file first")
    
    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                        padding: 3rem; border-radius: 20px; text-align: center; margin: 2rem 0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🌐</div>
                <h3 style="color: #2c3e50; font-size: 1.8rem; margin-bottom: 1rem;">Web Content Extraction</h3>
                <p style="color: #34495e; font-size: 1.1rem; margin-bottom: 2rem;">
                    Fetch and analyze articles directly from news websites and blogs
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            url_input = st.text_input(
                "Article URL", 
                placeholder="https://example.com/article", 
                key="url_input",
                help="Enter the full URL of the article you want to analyze"
            )
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("🌍 **Fetch & Analyze**", key="url_btn", use_container_width=True, type="primary"):
                    if url_input:
                        with st.spinner("🔄 Fetching content from web..."):
                            progress = st.progress(0)
                            for i in range(100):
                                time.sleep(0.015)
                                progress.progress(i + 1)
                            text_content = extract_text_from_url(url_input)
                            if text_content:
                                st.session_state.current_text = text_content
                                st.success("✅ Content fetched successfully!")
                                # st.balloons()
                                time.sleep(2)
                                st.session_state.current_page = "analytics"
                                st.rerun()
                    else:
                        st.error("⚠️ Please enter a valid URL")
    
    with tab3:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 3rem; border-radius: 20px; text-align: center; margin: 2rem 0;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">✍️</div>
                <h3 style="color: #2c3e50; font-size: 1.8rem; margin-bottom: 1rem;">Direct Text Input</h3>
                <p style="color: #34495e; font-size: 1.1rem; margin-bottom: 2rem;">
                    Paste or type your content directly for immediate analysis
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            text_input = st.text_area(
                "Your Text Content", 
                placeholder="Paste your article, news content, or any text you want to analyze...", 
                height=200, 
                key="text_input",
                help="Enter at least 50 characters for meaningful analysis"
            )
            
            # Character counter
            if text_input:
                char_count = len(text_input)
                word_count = len(text_input.split())
                st.markdown(f"""
                <div style="text-align: center; color: #7f8c8d; margin: 1rem 0;">
                    📝 {char_count} characters • {word_count} words
                </div>
                """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                if st.button("⚡ **Start Analysis**", key="text_btn", use_container_width=True, type="primary"):
                    if text_input and len(text_input.strip()) > 50:
                        st.session_state.current_text = text_input
                        st.success("✅ Text ready for analysis!")
                        # st.balloons()
                        time.sleep(2)
                        st.session_state.current_page = "analytics"
                        st.rerun()
                    elif text_input:
                        st.warning("⚠️ Please enter at least 50 characters for meaningful analysis")
                    else:
                        st.error("⚠️ Please enter some text content")
    
    # Features showcase
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h3 style="color: #2c3e50; font-size: 2rem; margin-bottom: 2rem;">✨ What You'll Get</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; max-width: 1000px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎯</div>
                <h4 style="margin-bottom: 1rem;">Smart Classification</h4>
                <p style="opacity: 0.9;">Automatically categorize your content with AI precision</p>
            </div>
            <div style="background: linear-gradient(135deg, #ffecd2, #fcb69f); color: #2c3e50; padding: 2rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📝</div>
                <h4 style="margin-bottom: 1rem;">Intelligent Summaries</h4>
                <p>Get concise, meaningful summaries of lengthy content</p>
            </div>
            <div style="background: linear-gradient(135deg, #a8edea, #fed6e3); color: #2c3e50; padding: 2rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔑</div>
                <h4 style="margin-bottom: 1rem;">Key Insights</h4>
                <p>Extract important keywords and topics automatically</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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