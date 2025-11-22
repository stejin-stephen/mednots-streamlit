import streamlit as st
from utils.database import get_all_notes, search_notes, filter_notes_by_specialty, get_note_by_id, delete_note, init_db
from utils.summarizer import format_soap_note, format_vitals, format_exam_findings
from datetime import datetime

st.set_page_config(page_title="Note History", page_icon="📚", layout="wide")

try:
    init_db()
except Exception:
    pass

st.title("📚 Note History")
st.markdown("View, search, and manage saved clinical notes")

try:
    init_db()
except Exception as e:
    st.error(f"⚠️ Database not available: {str(e)}")
    st.info("Unable to connect to the database. Please check your DATABASE_URL configuration.")
    st.stop()

col_search, col_filter = st.columns([2, 1])

with col_search:
    search_query = st.text_input("🔍 Search notes", placeholder="Search in note content...")

with col_filter:
    specialty_filter = st.selectbox(
        "Filter by Specialty",
        ["All", "General", "Cardiology", "Pediatrics", "Internal Medicine", "Emergency Medicine"]
    )

try:
    if search_query:
        notes = search_notes(search_query)
    elif specialty_filter != "All":
        notes = filter_notes_by_specialty(specialty_filter)
    else:
        notes = get_all_notes(100)
    
    if not notes:
        st.info("No saved notes found. Create and save notes from the Summarize page.")
        st.stop()
    
    st.markdown(f"### Found {len(notes)} note(s)")
    
    for note in notes:
        with st.expander(
            f"📋 Note #{note.id} - {note.specialty} - {note.created_at.strftime('%Y-%m-%d %H:%M') if note.created_at else 'N/A'}"
        ):
            col_note1, col_note2 = st.columns([2, 1])
            
            with col_note1:
                st.markdown("#### Original Note")
                st.text_area(
                    "Note content",
                    value=note.original_note[:500] + ("..." if len(note.original_note) > 500 else ""),
                    height=150,
                    key=f"note_orig_{note.id}",
                    disabled=True,
                    label_visibility="collapsed"
                )
            
            with col_note2:
                st.markdown("#### Actions")
                
                if st.button(f"👁️ View Full Note", key=f"view_{note.id}", use_container_width=True):
                    st.session_state[f'view_note_{note.id}'] = True
                
                if st.button(f"🗑️ Delete", key=f"delete_{note.id}", use_container_width=True, type="secondary"):
                    if delete_note(note.id):
                        st.success(f"Note #{note.id} deleted")
                        st.rerun()
                    else:
                        st.error("Failed to delete note")
            
            if st.session_state.get(f'view_note_{note.id}', False):
                st.markdown("---")
                st.markdown("### Full Note Details")
                
                tab1, tab2, tab3 = st.tabs(["📄 SOAP", "💉 Vitals", "🔍 Findings"])
                
                with tab1:
                    if note.soap_note:
                        soap_formatted = format_soap_note({"soap_note": note.soap_note})
                        st.markdown(soap_formatted)
                    else:
                        st.info("No SOAP data")
                
                with tab2:
                    if note.key_vitals:
                        vitals_formatted = format_vitals({"key_vitals": note.key_vitals})
                        st.markdown(vitals_formatted)
                    else:
                        st.info("No vitals data")
                
                with tab3:
                    if note.exam_findings:
                        findings_formatted = format_exam_findings({"exam_findings": note.exam_findings})
                        st.markdown(findings_formatted)
                    else:
                        st.info("No exam findings")
                
                if st.button("✖️ Close", key=f"close_{note.id}"):
                    st.session_state[f'view_note_{note.id}'] = False
                    st.rerun()

except Exception as e:
    st.error(f"Error loading notes: {str(e)}")
