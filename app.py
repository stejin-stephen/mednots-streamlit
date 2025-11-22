import streamlit as st
from utils.database import init_db

st.set_page_config(
    page_title="Home",
    page_icon="🏥",
    layout="wide"
)

try:
    init_db()
except Exception:
    pass

st.title("🏥 Medical Note Summarizer")

st.markdown("""
### Welcome to the Medical Note Summarization System

This AI-powered tool helps healthcare professionals transform unstructured clinical notes into structured SOAP format.

#### Features:
- **📝 Summarize Note**: Convert free-text clinical notes into structured SOAP format
- **📚 Note History**: View and manage saved clinical notes
- **📤 Bulk Processing**: Process multiple notes at once
- **⚙️ Settings**: Configure medical terminology validation

#### Getting Started:
1. Click **"Summarize Note"** in the sidebar to start processing clinical notes
2. Use example templates or paste your own notes
3. Review extracted vitals, exam findings, and SOAP format
4. Save notes to history for future reference

---

### Quick Links
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("#### 📝 Summarize")
    st.markdown("Process clinical notes into structured format")
    st.page_link("pages/1_Summarize_Note.py", label="Go to Summarize", icon="📝")

with col2:
    st.markdown("#### 📚 History")
    st.markdown("View saved notes and search history")
    st.page_link("pages/2_Note_History.py", label="Go to History", icon="📚")

with col3:
    st.markdown("#### 📤 Bulk")
    st.markdown("Process multiple notes at once")
    st.page_link("pages/3_Bulk_Processing.py", label="Go to Bulk", icon="📤")

with col4:
    st.markdown("#### ⚙️ Settings")
    st.markdown("Configure validation options")
    st.page_link("pages/4_Settings.py", label="Go to Settings", icon="⚙️")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85em;'>
    <p>🔒 AI-powered medical documentation</p>
    <p>Always verify output accuracy</p>
</div>
""", unsafe_allow_html=True)
