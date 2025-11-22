# Medical Note Summarizer

## Overview

A medical documentation application that transforms unstructured clinical notes into structured SOAP (Subjective, Objective, Assessment, Plan) format. The system extracts key medical information including vital signs, physical examination findings, and clinical assessments from free-text medical notes using AI-powered natural language processing.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
**Problem:** Need an accessible interface for medical professionals to input clinical notes and view structured outputs.

**Solution:** Streamlit-based web application with wide layout for comprehensive data display.

**Rationale:** Streamlit provides rapid development of data-focused applications with minimal frontend code, allowing medical professionals to interact with the summarization tool through a simple, intuitive interface without complex UI frameworks.

### Backend Architecture
**Problem:** Process unstructured medical text and extract structured medical information.

**Solution:** Python-based backend with modular utility structure separating concerns:
- `app.py` - Main Streamlit application entry point
- `utils/summarizer.py` - Core medical text processing and extraction logic
- `utils/openai_client.py` - AI service client management

**Rationale:** Separation of concerns allows independent testing and modification of summarization logic from the presentation layer. Python's rich ecosystem for medical NLP and data processing makes it ideal for this domain.

### AI Processing Pipeline
**Problem:** Convert unstructured clinical narratives into standardized SOAP format with extracted vitals and findings.

**Solution:** OpenAI GPT-5 model with structured JSON prompting for extracting:
- SOAP note components (Subjective, Objective, Assessment, Plan)
- Vital signs (BP, HR, temperature, RR, SpO2)
- Physical examination findings
- Patient demographics and chief complaint

**Rationale:** Large language models excel at understanding medical terminology and context. Structured JSON prompting ensures consistent, parseable outputs. GPT-5 provides state-of-the-art medical text understanding.

**Design Pattern:** The system uses a prompt engineering approach with explicit JSON schema definition to ensure reliable structured output from the AI model.

### Data Formatting
**Problem:** Present extracted medical information in clinically useful formats.

**Solution:** Dedicated formatting functions (`format_soap_note`, `format_vitals`, `format_exam_findings`) to structure AI outputs for display.

**Rationale:** Separating extraction from formatting allows flexibility in presentation while maintaining consistent data processing. Medical professionals require specific formatting standards for clinical documentation.

## External Dependencies

### AI Services
- **OpenAI API (GPT-5 model)** - Core NLP engine for medical text extraction and structuring
  - Configured via `AI_INTEGRATIONS_OPENAI_API_KEY` environment variable
  - Supports custom base URL via `AI_INTEGRATIONS_OPENAI_BASE_URL` for potential self-hosted or alternative endpoints
  - Used for transforming unstructured clinical notes into structured JSON format

### Python Frameworks
- **Streamlit** - Web application framework for the user interface
  - Provides rapid prototyping with minimal code
  - Built-in components for medical data visualization
  - Wide layout configuration for comprehensive data display

### Development Considerations
- Environment-based configuration for API credentials (no hardcoded secrets)
- Example clinical notes embedded in application for demonstration and testing
- Modular utility structure enables unit testing of individual components