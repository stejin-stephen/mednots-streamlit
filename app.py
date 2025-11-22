import streamlit as st
from utils.summarizer import extract_medical_summary, format_soap_note, format_vitals, format_exam_findings

st.set_page_config(
    page_title="Medical Note Summarizer",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medical Note Summarization Pipeline")
st.markdown("Transform unstructured clinical notes into structured SOAP format with key findings")

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

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Clinical Note")
    
    example_choice = st.selectbox(
        "Load Example Template:",
        ["Custom Note"] + list(EXAMPLE_NOTES.keys())
    )
    
    if example_choice != "Custom Note":
        default_text = EXAMPLE_NOTES[example_choice]
    else:
        default_text = ""
    
    clinical_note = st.text_area(
        "Enter clinical note:",
        value=default_text,
        height=400,
        placeholder="Enter unstructured clinical notes here...\n\nExample:\n65-year-old male with chest pain for 2 days..."
    )
    
    process_button = st.button("🔍 Generate Summary", type="primary", use_container_width=True)

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
    
    if 'last_result' in st.session_state:
        result = st.session_state['last_result']
        
        tab1, tab2, tab3, tab4 = st.tabs(["📄 SOAP Note", "💉 Vitals", "🔍 Exam Findings", "ℹ️ Key Info"])
        
        with tab1:
            soap_formatted = format_soap_note(result)
            st.markdown(soap_formatted)
            st.button("📋 Copy SOAP Note", key="copy_soap", on_click=lambda: st.write(""))
            with st.expander("View Raw Data"):
                st.json(result.get("soap_note", {}))
        
        with tab2:
            vitals_formatted = format_vitals(result)
            st.markdown(vitals_formatted)
            with st.expander("View Raw Data"):
                st.json(result.get("key_vitals", {}))
        
        with tab3:
            findings_formatted = format_exam_findings(result)
            st.markdown(findings_formatted)
            with st.expander("View Raw Data"):
                st.json(result.get("exam_findings", []))
        
        with tab4:
            key_info = result.get("key_information", {})
            if key_info:
                for key, value in key_info.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.info("No key information extracted")
            with st.expander("View Raw Data"):
                st.json(key_info)
    else:
        st.info("👈 Enter a clinical note and click 'Generate Summary' to see structured output")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>🔒 This tool uses AI to structure clinical notes. Always verify output for accuracy.</p>
    <p>Medical Note Summarization Pipeline | Powered by OpenAI via Replit AI Integrations</p>
</div>
""", unsafe_allow_html=True)
