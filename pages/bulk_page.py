import streamlit as st
from utils.summarizer import extract_medical_summary
from utils.database import save_clinical_note, init_db
import time

def render():
    st.title("📤 Bulk Note Processing")
    st.markdown("Upload and process multiple clinical notes simultaneously")
    
    st.info("💡 Upload a text file with multiple notes separated by '---' or upload multiple text files")
    
    upload_method = st.radio(
        "Upload Method",
        ["Single file with separator", "Multiple files"]
    )
    
    if upload_method == "Single file with separator":
        uploaded_file = st.file_uploader(
            "Upload text file (notes separated by ---)",
            type=['txt'],
            help="Each note should be separated by a line containing only ---"
        )
        
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            notes = [note.strip() for note in content.split('---') if note.strip()]
            
            st.success(f"Found {len(notes)} notes in file")
            
            if st.checkbox("Preview notes"):
                for i, note in enumerate(notes[:3], 1):
                    with st.expander(f"Note {i} preview"):
                        st.text(note[:300] + ("..." if len(note) > 300 else ""))
            
            specialty = st.selectbox(
                "Specialty for all notes",
                ["General", "Cardiology", "Pediatrics", "Internal Medicine", "Emergency Medicine"]
            )
            
            if st.button("🚀 Process All Notes", type="primary"):
                process_notes_bulk(notes, specialty)
    
    else:
        uploaded_files = st.file_uploader(
            "Upload multiple text files",
            type=['txt'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files")
            
            specialty = st.selectbox(
                "Specialty for all notes",
                ["General", "Cardiology", "Pediatrics", "Internal Medicine", "Emergency Medicine"]
            )
            
            if st.button("🚀 Process All Files", type="primary"):
                notes = []
                for file in uploaded_files:
                    content = file.read().decode('utf-8')
                    notes.append(content)
                process_notes_bulk(notes, specialty)

def process_notes_bulk(notes, specialty):
    init_db()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_container = st.container()
    
    successful = 0
    failed = 0
    
    for i, note in enumerate(notes):
        status_text.text(f"Processing note {i+1}/{len(notes)}...")
        
        try:
            result = extract_medical_summary(note)
            
            if "error" not in result:
                note_id = save_clinical_note(note, result, specialty)
                successful += 1
                with results_container:
                    st.success(f"✅ Note {i+1} processed and saved (ID: {note_id})")
            else:
                failed += 1
                with results_container:
                    st.error(f"❌ Note {i+1} failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            failed += 1
            with results_container:
                st.error(f"❌ Note {i+1} failed: {str(e)}")
        
        progress_bar.progress((i + 1) / len(notes))
        time.sleep(0.5)
    
    status_text.text("Processing complete!")
    st.success(f"✅ Successfully processed: {successful} | ❌ Failed: {failed}")
