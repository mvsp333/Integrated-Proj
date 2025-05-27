import streamlit as st
from utils.add_custom_css import add_custom_css
from utils.create_sliding_images import create_sliding_images
from nlp.extract_pdf_text import extract_text_from_pdf
from nlp.extract_url_text import extract_text_from_url
from nlp.classify import classify_text as classify_text
from nlp.summarize import extractive_summarization
from nlp.extract_keywords import extract_keywords
from nltk.tokenize import sent_tokenize


st.set_page_config(
    page_title="NewsSense - AI News Analysis",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_custom_css()

if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""

st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 1rem;">
        <h2>📰 NewsSense</h2>
        <p>AI-Powered News Analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio("Navigate to:", ["🏠 Home", "🔍 Analysis"], index=0)

if page == "🏠 Home":
    st.markdown(
        """
        <div class="main-header">
            <h1>📰 Welcome to NewsSense</h1>
            <h3>Intelligent News Classification & Summarization</h3>
            <p>Transform overwhelming news content into actionable insights</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🎬 Experience the Power of AI")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🎭 Show Dynamic News Analysis", key="animate"):
            create_sliding_images()

    st.markdown("---")
    st.markdown("### 📝 Choose Your Input Method")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='feature-card'><h4>📄 Upload PDF</h4></div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'], key="pdf_upload")
        if uploaded_file and st.button("📄 Process PDF", key="pdf_btn"):
            with st.spinner("🔄 Extracting text from PDF..."):
                text_content = extract_text_from_pdf(uploaded_file)
                if text_content:
                    st.session_state.current_text = text_content
                    st.success("✅ PDF processed successfully!")
                    st.info("🔍 Go to Analysis section to view results")

    with col2:
        st.markdown("<div class='feature-card'><h4>🔗 Paste URL</h4></div>", unsafe_allow_html=True)
        url_input = st.text_input("Enter article URL:", key="url_input")
        if url_input and st.button("🔗 Fetch & Analyze", key="url_btn"):
            with st.spinner("🔄 Fetching content from URL..."):
                text_content = extract_text_from_url(url_input)
                if text_content:
                    st.session_state.current_text = text_content
                    st.success("✅ Content fetched successfully!")
                    st.info("🔍 Go to Analysis section to view results")

    with col3:
        st.markdown("<div class='feature-card'><h4>✏️ Direct Text</h4></div>", unsafe_allow_html=True)
        text_input = st.text_area("Paste your article:", height=150, key="text_input")
        if text_input and st.button("✏️ Analyze Text", key="text_btn"):
            st.session_state.current_text = text_input
            st.success("✅ Text ready for analysis!")
            st.info("🔍 Go to Analysis section to view results")

elif page == "🔍 Analysis":
    st.markdown(
        """
        <div class="main-header">
            <h1>🔍 News Analysis Results</h1>
            <p>Comprehensive AI-powered analysis of your content</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.current_text:
        st.warning("⚠️ No content to analyze. Please go to Home and select an input method.")
        st.info("👈 Use the sidebar to navigate back to Home")
    else:
        text_content = st.session_state.current_text

        with st.spinner("🤖 Analyzing content with AI..."):
            category = classify_text(text_content)
            summary = extractive_summarization(text_content)
            keywords = extract_keywords(text_content)

            st.session_state.analysis_data = {
                'text': text_content,
                'category': category,
              
                'summary': summary,
                'keywords': keywords
            }

        results = st.session_state.analysis_data

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='metric-card'><h4>Category</h4><h2>{results['category'].title()}</h2></div>", unsafe_allow_html=True)

        # with col2:
        #     st.markdown(f"<div class='metric-card'><h4>Confidence</h4><h2>{results['confidence']:.1%}</h2></div>", unsafe_allow_html=True)

        with col2:
            word_count = len(text_content.split())
            st.markdown(f"<div class='metric-card'><h4>Word Count</h4><h2>{word_count}</h2></div>", unsafe_allow_html=True)

        with col3:
            sentence_count = len(sent_tokenize(text_content))
            st.markdown(f"<div class='metric-card'><h4>Sentences</h4><h2>{sentence_count}</h2></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📄 Extracted Text")
        st.markdown(f"<div class='analysis-card'><p>{text_content[:1500]}{'...' if len(text_content) > 1500 else ''}</p></div>", unsafe_allow_html=True)
        if len(text_content) > 1500:
            with st.expander("📖 View Full Text"):
                st.write(text_content)

        st.markdown("### 📝 AI-Generated Summary")
        st.markdown(f"<div class='analysis-card'><p>{results['summary']}</p></div>", unsafe_allow_html=True)

        st.markdown("### 🔑 Extracted Keywords")
        if results['keywords']:
            keyword_tags = "".join(
                f"<span style='background: linear-gradient(90deg, #667eea, #764ba2); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; margin: 0.2rem; display: inline-block;'>{kw}</span>"
                for kw in results['keywords'][:10]
            )
            st.markdown(f"<div class='analysis-card'>{keyword_tags}</div>", unsafe_allow_html=True)
        else:
            st.info("No keywords extracted from the text.")
