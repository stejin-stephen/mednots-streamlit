# Medical Note Summarizer

A comprehensive medical documentation application that transforms unstructured clinical notes into structured SOAP (Subjective, Objective, Assessment, Plan) format using AI-powered natural language processing.

![Medical Note Summarizer](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.11-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)

## Features

- **🎤 Audio Transcription**: Record audio in-app or upload audio files and automatically transcribe them to text using OpenAI Whisper
- **📄 Lab Report OCR**: Upload lab reports and medical documents (PDF, JPG, PNG) and extract text using AI-powered OCR via OpenAI Vision
- **AI-Powered Summarization**: Transform free-text clinical notes into structured SOAP format using OpenAI GPT-5
- **Automated Extraction**: Automatically extract vital signs, physical examination findings, and clinical assessments
- **Note History**: Save and search through all processed notes with PostgreSQL database persistence
- **Bulk Processing**: Upload and process multiple clinical notes simultaneously
- **Multi-Format Exports**: Export notes to PDF, Word (DOCX), HL7 FHIR JSON, and EMR JSON formats
- **Specialty Templates**: Support for specialty-specific output templates (Cardiology, Pediatrics, Internal Medicine, Emergency Medicine)
- **Medical Terminology**: UI for configuring validation and standardization options

## Screenshots

### Summarize Note
Transform unstructured clinical notes into structured SOAP format with extracted vitals and exam findings.

### Note History
View, search, and manage all saved clinical notes with filtering by specialty.

### Bulk Processing
Process multiple clinical notes at once with progress tracking.

## Quick Start

For complete beginners, here's the fastest way to get started:

```bash
# 1. Download the project (see "Get the Code" section below)
# 2. Navigate to the project folder
cd medical-note-summarizer

# 3. Install Python dependencies
pip install streamlit openai sqlalchemy psycopg2-binary reportlab python-docx fhir-resources

# 4. Copy the environment template and add your API keys
cp .env.example .env
# Edit .env and add your OpenAI API key and database URL

# 5. Run the application
streamlit run app.py --server.port 5000

# 6. Open your browser to http://localhost:5000
```

**That's it!** You should see the Medical Note Summarizer running locally.

## Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Services**: 
  - OpenAI GPT-5 for medical text extraction and SOAP formatting
  - OpenAI Whisper for audio-to-text transcription
  - OpenAI Vision (GPT-4o) for OCR and document text extraction
- **Database**: PostgreSQL (Neon-backed) with SQLAlchemy ORM
- **Document Generation**: ReportLab (PDF), python-docx (Word), fhir.resources (HL7 FHIR)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11 or higher
- PostgreSQL database (or use a cloud provider like Neon, Supabase, etc.)
- OpenAI API key (for GPT-5 access)

## Local Setup

### 1. Get the Code

**Option A: Clone from Git**
```bash
git clone <your-repository-url>
cd medical-note-summarizer
```

**Option B: Download from Replit**
If this project is on Replit, you can download it as a ZIP:
1. Open your Repl
2. Click the three dots menu (•••)
3. Select "Download as zip"
4. Extract the ZIP file to your local machine

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

This project uses modern Python dependency management with `pyproject.toml`. Choose one of the following methods:

#### Option A: Using pip (recommended for most users)

```bash
# Install all dependencies from pyproject.toml
pip install .
```

Or install packages individually:

```bash
pip install streamlit>=1.51.0 openai>=2.8.1 sqlalchemy>=2.0.44 psycopg2-binary>=2.9.11 reportlab>=4.4.5 python-docx>=1.2.0 fhir-resources>=8.1.0
```

#### Option B: Using uv (faster, modern alternative)

```bash
# Install uv package manager
pip install uv

# Install dependencies
uv pip install -e .
```

#### Option C: Generate requirements.txt (for legacy compatibility)

```bash
# Generate requirements.txt from pyproject.toml
pip install pip-tools
pip-compile pyproject.toml -o requirements.txt
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
# Copy the template
cp .env.example .env

# Edit the .env file with your actual credentials
nano .env  # or use any text editor
```

Fill in your actual values in the `.env` file:

```bash
# Required: Your OpenAI API key
AI_INTEGRATIONS_OPENAI_API_KEY=sk-proj-your-actual-key-here

# Required: Your PostgreSQL database connection
DATABASE_URL=postgresql://username:password@localhost:5432/medical_notes
```

**Important Notes:**
- The `.env.example` file is a template - never put real credentials in it
- Your actual `.env` file is already listed in `.gitignore` and won't be committed
- Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- For local PostgreSQL, ensure the database `medical_notes` exists (see next step)

### 5. Set Up the Database

The application will automatically create the required database tables on first run. However, you need to ensure your PostgreSQL database exists:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE medical_notes;

# Exit PostgreSQL
\q
```

### 6. Run the Application

```bash
streamlit run app.py --server.port 5000
```

The application will be available at `http://localhost:5000`

## Project Structure

```
medical-note-summarizer/
├── app.py                      # Main entry point and home page
├── pages/                      # Streamlit multi-page structure
│   ├── Summarize_Note.py      # Main summarization page
│   ├── Note_History.py        # Saved notes with search/filter
│   ├── Bulk_Processing.py    # Batch note processing
│   └── Settings.py            # Configuration settings
├── utils/                      # Utility modules
│   ├── summarizer.py          # Core AI summarization logic
│   ├── openai_client.py       # OpenAI API client
│   ├── database.py            # Database operations (SQLAlchemy)
│   └── export.py              # PDF, Word, FHIR export functions
├── .streamlit/                 # Streamlit configuration
│   └── config.toml            # Server and theme settings
├── pyproject.toml              # Python dependencies and project config
├── uv.lock                     # Lock file for reproducible installs
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules (excludes .env, __pycache__, etc.)
└── README.md                   # This file (you are here!)
```

## Usage

### 1. Summarize a Clinical Note

#### Option A: Text Input
1. Navigate to **Summarize Note** from the sidebar
2. Choose an example template or enter your own clinical note
3. Select a specialty (General, Cardiology, Pediatrics, etc.)
4. Click **Generate Summary**
5. Review the structured SOAP note, vitals, and exam findings
6. Click **Save to History** to store the note in the database

#### Option B: Multi-Modal Input (New!)

You can provide clinical information in multiple ways:

**Method 1: Record Audio In-App**
1. Navigate to **Summarize Note** from the sidebar
2. Click the **Record Audio** tab
3. Click the microphone button to start recording your clinical note
4. Click again to stop recording
5. Click **Transcribe Recording** to convert speech to text using Whisper AI
6. Review and edit the transcribed text if needed
7. Select a specialty and click **Generate Summary**

**Method 2: Upload Audio File**
1. Navigate to **Summarize Note** from the sidebar
2. Click the **Upload Audio** tab
3. Upload a pre-recorded audio file (MP3, WAV, M4A, etc.)
4. Click **Transcribe Upload** to convert speech to text using Whisper AI
5. Review and edit the transcribed text if needed
6. Select a specialty and click **Generate Summary**

**Method 3: Upload Lab Report (OCR)**
1. Navigate to **Summarize Note** from the sidebar
2. Click the **Upload Lab Report** tab
3. Upload a lab report or medical document (PDF, JPG, or PNG)
4. Preview the document (images show preview, PDFs show file info)
5. Click **Extract Text (OCR)** to extract text using AI-powered OCR
6. Review and edit the extracted text if needed
7. Select a specialty and click **Generate Summary**

#### Option C: View and Download EMR JSON (New!)

After generating a summary, you can view and download the structured EMR JSON format:

1. Navigate to the **📊 EMR JSON** tab in the structured output section
2. Review the JSON structure containing:
   - **presenting_complaint**: Chief complaint/reason for visit
   - **patient_demographics**: Age and gender
   - **subjective**: Patient-reported symptoms
   - **vital_signs**: All extracted vitals (BP, HR, temp, RR, SpO2)
   - **physical_examination**: Exam findings
   - **diagnosis**: Diagnosis with ICD codes (pending integration)
   - **plan**: Treatment plan
   - **assessment_notes**: Clinical assessment
   - **symptom_duration**: Duration of symptoms
3. Click **📥 Download EMR JSON** to save the file
4. Use the JSON in your EMR/EHR systems or for further processing

**Sample EMR JSON:**
```json
{
  "presenting_complaint": "chest pain",
  "patient_demographics": {
    "age": "65",
    "gender": "male"
  },
  "vital_signs": {
    "blood_pressure": "145/92 mmHg",
    "heart_rate": "88 bpm",
    "temperature": "98.4°F",
    "respiratory_rate": "18 breaths/min",
    "oxygen_saturation": "96%"
  },
  "diagnosis": [
    { "code": "Pending", "text": "Acute inferior wall myocardial infarction" }
  ],
  "plan": "Activate cath lab, Aspirin 325mg, Plavix 600mg..."
}
```

### 2. View Note History

1. Navigate to **Note History** from the sidebar
2. Search notes by content using the search box
3. Filter notes by specialty
4. Click on any note to view full details
5. Export individual notes or delete unwanted entries

### 3. Bulk Processing

1. Navigate to **Bulk Processing** from the sidebar
2. Upload a text file containing multiple clinical notes (one per note, separated by blank lines or delimiters)
3. Select a specialty for all notes
4. Click **Process Notes**
5. View progress and results for all processed notes

### 4. Configure Settings

1. Navigate to **Settings** from the sidebar
2. Configure medical terminology validation options
3. Set export preferences (PDF layout, FHIR version)
4. Manage custom templates (future feature)

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `AI_INTEGRATIONS_OPENAI_API_KEY` | Yes | OpenAI API key for GPT-5 access | `sk-proj-...` |
| `AI_INTEGRATIONS_OPENAI_BASE_URL` | No | OpenAI API base URL (default: OpenAI official) | `https://api.openai.com/v1` |
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/dbname` |
| `SESSION_SECRET` | No | Secret key for session management | Any random string |

## Deployment

### Deploy to Replit

This project is optimized for deployment on Replit:

1. Import this repository to Replit
2. Replit will automatically detect dependencies and set up the environment
3. Configure secrets in the Replit Secrets panel:
   - `AI_INTEGRATIONS_OPENAI_API_KEY`
   - `DATABASE_URL` (provided automatically by Replit PostgreSQL)
4. Click "Run" to start the application
5. Use the "Publish" button to deploy publicly

### Deploy to Other Platforms

**Streamlit Cloud:**
```bash
# Add secrets in Streamlit Cloud dashboard
# Deploy directly from GitHub repository
```

**Heroku:**
```bash
# Create Procfile
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

# Deploy using Heroku CLI
heroku create your-app-name
git push heroku main
```

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
```

## API Keys and Security

**Important Security Notes:**
- Never commit API keys or secrets to version control
- Always use environment variables for sensitive configuration
- Use `.gitignore` to exclude `.env` files
- For production deployments, use secure secret management services
- The OpenAI API key will incur costs based on usage

**Getting an OpenAI API Key:**
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new API key
4. Add billing information (GPT-5 and Whisper require a paid account)
5. Store the key securely in your environment variables

**Note**: The same API key works for GPT-5 (text summarization), Whisper (audio transcription), and Vision (OCR).

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests (if test files exist)
pytest tests/
```

### Code Style

This project follows Python PEP 8 style guidelines. Format code using:

```bash
pip install black
black .
```

## Troubleshooting

### Database Connection Issues

If you see "Database not available" errors:
1. Verify PostgreSQL is running: `pg_isready`
2. Check DATABASE_URL is correctly formatted
3. Ensure the database exists and is accessible
4. Check firewall rules if using remote database

### OpenAI API Errors

If summarization, transcription, or OCR fails:
1. Verify your API key is valid and active
2. Check you have sufficient credits in your OpenAI account
3. Ensure you have access to GPT-5, Whisper, and GPT-4o (Vision) models
4. Check network connectivity to OpenAI API
5. For audio files, ensure they are under 25 MB and in a supported format
6. For documents, ensure PDFs are under 5 pages and images are clear/readable

### Audio Transcription Issues

**In-App Recording:**
If browser recording doesn't work:
1. Grant microphone permissions when prompted by your browser
2. Ensure your device has a working microphone
3. Try a different browser (Chrome, Firefox, Edge recommended)
4. Check that no other application is blocking microphone access

**File Upload:**
If audio upload doesn't work:
1. Ensure the audio file is in a supported format (MP3, WAV, M4A, etc.)
2. Check the file size is under 25 MB (Whisper API limit)
3. Verify your OpenAI API key has access to the Whisper model
4. Try converting the audio to MP3 if using an uncommon format

### Lab Report OCR Issues

If document text extraction doesn't work:
1. Ensure the document is in a supported format (PDF, JPG, PNG)
2. Check that the document is clear and readable (not blurry or low-resolution)
3. For PDFs, limit to 5 pages or less for optimal performance
4. Verify your OpenAI API key has access to GPT-4o (Vision) model
5. Try converting handwritten notes to typed documents for better accuracy
6. Ensure medical terminology is legible in the original document

### Streamlit Port Already in Use

If port 5000 is occupied:
```bash
streamlit run app.py --server.port 8501
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

**Medical Disclaimer**: This tool is for demonstration and educational purposes only. Always verify AI-generated medical documentation with qualified healthcare professionals. Do not use this tool as a substitute for professional medical judgment or for making clinical decisions.

## Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Contact the maintainers
- Check the documentation in `replit.md`

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenAI GPT-5](https://openai.com/)
- Database by [PostgreSQL](https://www.postgresql.org/)
- HL7 FHIR resources by [fhir.resources](https://pypi.org/project/fhir.resources/)

---

Made with ❤️ for healthcare professionals
