import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Medical Note Summarizer",
    page_icon="🏥",
    layout="wide"
)

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Summarize'

st.sidebar.title("🏥 Medical Note System")
page = st.sidebar.radio(
    "Navigation",
    ["📝 Summarize Note", "📚 Note History", "📤 Bulk Processing", "⚙️ Settings"],
    label_visibility="collapsed"
)

if page == "📝 Summarize Note":
    from pages import summarize_page
    summarize_page.render()
elif page == "📚 Note History":
    from pages import history_page
    history_page.render()
elif page == "📤 Bulk Processing":
    from pages import bulk_page
    bulk_page.render()
elif page == "⚙️ Settings":
    from pages import settings_page
    settings_page.render()

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85em;'>
    <p>🔒 AI-powered medical documentation</p>
    <p>Always verify output accuracy</p>
</div>
""", unsafe_allow_html=True)
