import streamlit as st
from utils.summarizer import extract_medical_summary, format_soap_note, format_vitals, format_exam_findings
from utils.database import save_clinical_note, init_db
from utils.export import export_to_pdf, export_to_word, export_to_fhir
from utils.openai_client import transcribe_audio
from datetime import datetime
import io
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Summarize Note", page_icon="📝", layout="wide")

try:
    init_db()
except Exception:
    pass

EXAMPLE_NOTES = {
    "Chest Pain": """65-year-old male with chest pain for 2 days. Patient reports substernal chest pressure, 7/10 severity, radiating to left arm. Worse with exertion, relieved by rest. Associated with shortness of breath and diaphoresis. No nausea or vomiting.

PMH: Hypertension, hyperlipidemia, Type 2 diabetes
Medications: Lisinopril 10mg daily, Atorvastatin 40mg daily, Metformin 1000mg BID
Allergies: NKDA

Vitals: BP 145/92, HR 88, Temp 98.4°F, RR 18, SpO2 96% on room air

Physical Exam:
General: Alert, anxious-appearing male in mild distress
Cardiovascular: Regular rate and rhythm, no murmurs. Mild jugular venous distension.
Respiratory: Clear to auscultation bilaterally, no wheezes or crackles
Extremities: No edema, pulses 2+ bilaterally

EKG: ST-segment elevation in leads II, III, aVF

Assessment: Acute inferior wall myocardial infarction

Plan:
1. Activate cath lab for emergent cardiac catheterization
2. Aspirin 325mg chewed, Plavix 600mg loading dose
3. Heparin bolus and infusion per protocol
4. Nitroglycerin sublingual PRN for chest pain
5. Serial troponins, CBC, BMP, lipid panel
6. Continuous cardiac monitoring
7. Cardiology consult""",

    "Pediatric Fever": """3-year-old female brought in by parents for fever and cough for 3 days. Mother reports temperature up to 102.5°F at home. Non-productive cough, runny nose, decreased appetite. No vomiting or diarrhea. Drinking adequate fluids. Up to date on immunizations.

Vitals: Temp 101.8°F, HR 120, RR 28, SpO2 98% on RA, Weight 15 kg

Physical Exam:
General: Well-appearing, playful child
HEENT: Bilateral tympanic membranes clear, erythematous posterior pharynx, no exudates
Neck: No lymphadenopathy
Lungs: Clear bilaterally, good air movement
Heart: RRR, no murmur
Abdomen: Soft, non-tender

Assessment: Viral upper respiratory infection

Plan:
1. Supportive care with rest and hydration
2. Acetaminophen 240mg (15mg/kg) every 6 hours PRN fever
3. Return if fever persists >5 days or develops difficulty breathing
4. Parent education provided""",

    "Annual Wellness": """52-year-old female for annual wellness visit. Patient feels well overall. No new complaints. Exercises 3x weekly, balanced diet. Non-smoker, occasional alcohol use.

PMH: Hypothyroidism
Medications: Levothyroxine 75mcg daily
FH: Mother with breast cancer at age 58, father with CAD

Vitals: BP 118/76, HR 68, Temp 98.2°F, BMI 24.3

Physical Exam:
General: Well-appearing, no acute distress
HEENT: Normal exam
Cardiovascular: RRR, no murmurs
Respiratory: CTAB
Breast: No masses, discharge, or skin changes
Abdomen: Soft, non-tender, no masses

Labs: TSH 2.1 (normal), Lipid panel WNL, A1c 5.4%

Assessment: Healthy adult, well-controlled hypothyroidism

Plan:
1. Continue current thyroid medication
2. Mammogram ordered (age-appropriate screening)
3. Discussed colorectal cancer screening options, patient prefers colonoscopy
4. Updated immunizations: Tdap, influenza
5. Return in 1 year for annual visit"""
}

SPECIALTY_TEMPLATES = {
    "General": "Standard SOAP format",
    "Cardiology": "Cardiology-focused template with detailed cardiac assessment",
    "Pediatrics": "Pediatric template with growth and development tracking",
    "Internal Medicine": "Comprehensive internal medicine assessment",
    "Emergency Medicine": "Emergency department note format"
}

st.title("🏥 Medical Note Summarization")
st.markdown("Transform unstructured clinical notes into structured SOAP format with key findings")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Clinical Note")
    
    col_ex, col_spec = st.columns(2)
    with col_ex:
        example_choice = st.selectbox(
            "Load Example Template:",
            ["Custom Note"] + list(EXAMPLE_NOTES.keys())
        )
    
    with col_spec:
        specialty = st.selectbox(
            "Specialty:",
            list(SPECIALTY_TEMPLATES.keys())
        )
    
    # Audio section with tabs for recording and uploading
    st.markdown("---")
    st.markdown("**🎤 Audio Note Input (Optional)**")
    st.caption("Record audio in-app or upload a file to automatically transcribe using Whisper AI")
    
    # Initialize transcription state
    if 'transcribed_text' not in st.session_state:
        st.session_state['transcribed_text'] = ""
    
    # Create tabs for recording vs uploading
    audio_tab1, audio_tab2 = st.tabs(["🎙️ Record Audio", "📁 Upload Audio File"])
    
    with audio_tab1:
        st.caption("Click the microphone to start/stop recording")
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="3x",
        )
        
        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")
            
            if st.button("🎧 Transcribe Recording", type="secondary", use_container_width=True, key="transcribe_recording"):
                with st.spinner("Transcribing your recording with Whisper AI..."):
                    # Convert to BytesIO for API
                    audio_io = io.BytesIO(audio_bytes)
                    
                    # Transcribe
                    result = transcribe_audio(audio_io, "recording.wav")
                    
                    if result.get("success"):
                        # Update the clinical note input session state so it appears in the text area
                        st.session_state['clinical_note_input'] = result["text"]
                        st.session_state['transcribed_text'] = result["text"]
                        st.success("✅ Recording transcribed successfully! Review the text below.")
                        st.rerun()
                    else:
                        st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")
    
    with audio_tab2:
        audio_file = st.file_uploader(
            "Choose an audio file",
            type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
            help="Supported formats: MP3, MP4, MPEG, M4A, WAV, WebM (max 25 MB)",
            label_visibility="collapsed"
        )
        
        # Transcribe audio if uploaded
        if audio_file is not None:
            if st.button("🎧 Transcribe Upload", type="secondary", use_container_width=True, key="transcribe_upload"):
                with st.spinner("Transcribing audio with Whisper AI..."):
                    # Create a BytesIO object from the uploaded file
                    audio_bytes_upload = io.BytesIO(audio_file.read())
                    
                    # Transcribe
                    result = transcribe_audio(audio_bytes_upload, audio_file.name)
                    
                    if result.get("success"):
                        # Update the clinical note input session state so it appears in the text area
                        st.session_state['clinical_note_input'] = result["text"]
                        st.session_state['transcribed_text'] = result["text"]
                        st.success("✅ Audio transcribed successfully! Review the text below.")
                        st.rerun()
                    else:
                        st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")
    
    st.markdown("---")
    
    # Initialize the clinical note input key if not present
    if 'clinical_note_input' not in st.session_state:
        if example_choice != "Custom Note":
            st.session_state['clinical_note_input'] = EXAMPLE_NOTES[example_choice]
        else:
            st.session_state['clinical_note_input'] = ""
    
    # Update clinical note input when example is selected (only if not already transcribed)
    if example_choice != "Custom Note" and not st.session_state.get('transcribed_text'):
        st.session_state['clinical_note_input'] = EXAMPLE_NOTES[example_choice]
    
    clinical_note = st.text_area(
        "Enter or review clinical note:",
        height=400,
        placeholder="Enter unstructured clinical notes here...\n\nOr upload an audio file above to transcribe automatically.\n\nExample:\n65-year-old male with chest pain for 2 days...",
        key="clinical_note_input"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        process_button = st.button("🔍 Generate Summary", type="primary", use_container_width=True)
    with col_btn2:
        save_button = st.button("💾 Save to History", use_container_width=True, disabled='last_result' not in st.session_state)

with col2:
    st.subheader("📋 Structured Output")
    
    if process_button and clinical_note.strip():
        with st.spinner("Processing clinical note..."):
            result = extract_medical_summary(clinical_note)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.session_state['last_result'] = result
                st.session_state['last_note'] = clinical_note
                st.session_state['current_specialty'] = specialty
    
    if save_button and 'last_result' in st.session_state:
        try:
            init_db()
            note_id = save_clinical_note(
                st.session_state['last_note'],
                st.session_state['last_result'],
                st.session_state.get('current_specialty', 'General')
            )
            st.success(f"✅ Note saved to history (ID: {note_id})")
        except Exception as e:
            st.error(f"Error saving note: {str(e)}")
    
    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 SOAP Note", "💉 Vitals", "🔍 Exam Findings", "ℹ️ Key Info", "📤 Export"])
        
        with tab1:
            soap_formatted = format_soap_note(result)
            st.markdown(soap_formatted)
            
            st.code(soap_formatted, language=None)
        
        with tab2:
            vitals_formatted = format_vitals(result)
            st.markdown(vitals_formatted)
        
        with tab3:
            findings_formatted = format_exam_findings(result)
            st.markdown(findings_formatted)
        
        with tab4:
            key_info = result.get("key_information", {})
            if key_info:
                for key, value in key_info.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.info("No key information extracted")
        
        with tab5:
            st.markdown("### Export Options")
            
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            
            with col_exp1:
                if st.button("📄 Export PDF", use_container_width=True):
                    try:
                        pdf_buffer = export_to_pdf(result, result, result, result.get("key_information", {}))
                        st.download_button(
                            label="Download PDF",
                            data=pdf_buffer,
                            file_name=f"medical_note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
            
            with col_exp2:
                if st.button("📝 Export Word", use_container_width=True):
                    try:
                        word_buffer = export_to_word(result, result, result, result.get("key_information", {}))
                        st.download_button(
                            label="Download Word",
                            data=word_buffer,
                            file_name=f"medical_note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error generating Word document: {str(e)}")
            
            with col_exp3:
                if st.button("🔗 Export FHIR", use_container_width=True):
                    try:
                        fhir_json = export_to_fhir(result, result, result, result.get("key_information", {}))
                        st.download_button(
                            label="Download FHIR JSON",
                            data=fhir_json,
                            file_name=f"medical_note_fhir_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Error generating FHIR: {str(e)}")
    else:
        st.info("👈 Enter a clinical note and click 'Generate Summary' to see structured output")
