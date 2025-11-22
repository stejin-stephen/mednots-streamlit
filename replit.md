# Medical Note Summarizer

## Overview

A comprehensive medical documentation application that transforms unstructured clinical notes into structured SOAP (Subjective, Objective, Assessment, Plan) format. The system extracts key medical information including vital signs, physical examination findings, and clinical assessments from free-text medical notes using AI-powered natural language processing. Features include note history with database persistence, bulk processing, multi-format exports (PDF, Word, FHIR), and specialty-specific templates.

## Recent Changes (November 2025)

### Enhanced Features
- **Audio Transcription**: Upload audio clinical notes and automatically transcribe using OpenAI Whisper (November 22, 2025)
- **Multi-page Navigation**: Added sidebar navigation with dedicated pages for Summarize, Note History, Bulk Processing, and Settings
- **Database Integration**: PostgreSQL database for persistent note storage with search and filtering capabilities
- **Bulk Processing**: Upload and process multiple clinical notes simultaneously with progress tracking
- **Export Functionality**: Export notes to PDF, Word (DOCX), and HL7 FHIR JSON formats
- **Specialty Templates**: Support for specialty-specific output templates (Cardiology, Pediatrics, Internal Medicine, Emergency Medicine)
- **Medical Terminology Settings**: UI for configuring validation and standardization options (foundational UI implemented)

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Multi-Page Application Structure
**Problem:** Need to organize multiple features (summarization, history, bulk processing, exports) in an intuitive interface.

**Solution:** Streamlit multi-page architecture with conditional rendering:
- `app.py` - Main entry point with sidebar navigation
- `pages/summarize_page.py` - Clinical note input and AI-powered summarization
- `pages/history_page.py` - Saved notes with search and filtering
- `pages/bulk_page.py` - Batch note processing with file upload
- `pages/settings_page.py` - Configuration for validation and export options

**Rationale:** Separating functionality into distinct pages improves user experience and code maintainability while keeping all features accessible from a single application.

### Backend Architecture
**Problem:** Process unstructured medical text, persist data, and provide multiple export formats.

**Solution:** Python-based backend with modular utility structure:
- `app.py` - Main Streamlit application with navigation
- `utils/summarizer.py` - Core medical text processing and extraction logic
- `utils/openai_client.py` - AI service client management
- `utils/database.py` - PostgreSQL database operations using SQLAlchemy
- `utils/export.py` - PDF, Word, and FHIR export functionality

**Rationale:** Clear separation of concerns allows independent testing and modification of each component. Modular design supports feature extension without impacting existing functionality.

### Database Layer
**Problem:** Persist clinical notes for historical review, search, and analysis.

**Solution:** PostgreSQL database with SQLAlchemy ORM:
- `ClinicalNote` model with fields for original text, extracted SOAP data, vitals, findings, and specialty
- Indexed search capabilities on note content
- Filtering by specialty and date
- Graceful degradation when database is unavailable

**Rationale:** PostgreSQL provides robust data persistence with ACID guarantees. SQLAlchemy ORM simplifies database operations while maintaining type safety. Storing both original and structured data enables future analysis and auditing.

### AI Processing Pipeline
**Problem:** Convert unstructured clinical narratives into standardized SOAP format with extracted vitals and findings.

**Solution:** OpenAI GPT-5 model with structured JSON prompting for extracting:
- SOAP note components (Subjective, Objective, Assessment, Plan)
- Vital signs (BP, HR, temperature, RR, SpO2)
- Physical examination findings
- Patient demographics and chief complaint

**Rationale:** Large language models excel at understanding medical terminology and context. Structured JSON prompting ensures consistent, parseable outputs. GPT-5 provides state-of-the-art medical text understanding.

**Design Pattern:** The system uses prompt engineering with explicit JSON schema definition to ensure reliable structured output from the AI model.

### Export System
**Problem:** Provide clinical notes in industry-standard formats for EHR integration and documentation.

**Solution:** Multi-format export utilities:
- **PDF Export**: ReportLab-based generation with styled headers, tables, and sections
- **Word Export**: python-docx for DOCX generation with proper formatting and structure
- **FHIR Export**: HL7 FHIR R4 Composition resources using fhir.resources library

**Rationale:** Different healthcare systems require different formats. PDF for printing, Word for editing, and FHIR for interoperability with electronic health records. All exports preserve the structured SOAP data.

### Data Formatting
**Problem:** Present extracted medical information in clinically useful formats.

**Solution:** Dedicated formatting functions (`format_soap_note`, `format_vitals`, `format_exam_findings`) to structure AI outputs for display.

**Rationale:** Separating extraction from formatting allows flexibility in presentation while maintaining consistent data processing. Medical professionals require specific formatting standards for clinical documentation.

## External Dependencies

### AI Services
- **OpenAI API (GPT-5 model)** - Core NLP engine for medical text extraction and structuring
  - Configured via `AI_INTEGRATIONS_OPENAI_API_KEY` environment variable
  - Supports custom base URL via `AI_INTEGRATIONS_OPENAI_BASE_URL`
  - Used for transforming unstructured clinical notes into structured JSON format
  - Accessed through Replit AI Integrations (no personal API key required)

### Database
- **PostgreSQL (Neon-backed)** - Data persistence for note history
  - Configured via `DATABASE_URL` environment variable
  - SQLAlchemy ORM for database operations
  - Automatic schema creation via `init_db()`

### Python Frameworks
- **Streamlit** - Web application framework for the user interface
  - Multi-page navigation with sidebar
  - Session state for data persistence across interactions
  - Built-in components for medical data visualization
  - Wide layout configuration for comprehensive data display

### Document Generation
- **ReportLab** - PDF generation with professional formatting
- **python-docx** - Microsoft Word document creation
- **fhir.resources** - HL7 FHIR resource generation for healthcare interoperability

## Development Considerations
- Environment-based configuration for all credentials (no hardcoded secrets)
- Example clinical notes embedded in application for demonstration and testing
- Modular utility structure enables unit testing of individual components
- Database operations include graceful error handling for missing configuration
- Export functions generate BytesIO buffers for efficient download handling
- Session state management preserves user work across page navigation

## Feature Completeness

### Implemented Features
✅ Text input area for clinical notes with example templates
✅ AI-powered SOAP format extraction using GPT-5
✅ Automated extraction of key vitals and exam findings
✅ Clean medical-themed multi-page interface
✅ Note history with database persistence
✅ Search and filter capabilities for saved notes
✅ Bulk note processing with file upload
✅ Specialty-specific templates (Cardiology, Pediatrics, Internal Medicine, etc.)
✅ PDF export functionality
✅ Word (DOCX) export functionality
✅ HL7 FHIR JSON export functionality
✅ Medical terminology validation UI (settings interface)

### Technical Debt & Future Enhancements
- Medical terminology validation backend (ICD-10, SNOMED CT, LOINC integration)
- Custom template creation and management
- User authentication and multi-user support
- Advanced analytics on saved notes
- Integration with external EHR systems
