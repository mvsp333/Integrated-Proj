import time
import streamlit as st

def create_sliding_images():
    """Create sliding news images effect"""
    news_images = [
        "📰", "📻", "📺", "💻", "📱", "🗞️", "📋", "📊", "🎯", "🚀"
    ]

    image_placeholder = st.empty()

    for i in range(len(news_images)):
        with image_placeholder.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(
                    f"""
                    <div style="text-align: center; font-size: 8rem; animation: pulse 1s infinite;">
                        {news_images[i]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        time.sleep(0.8)