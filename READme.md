# EduGenie - Google Gemini Powered Learning Assistant

EduGenie is a FastAPI educational assistant with a simple HTML/CSS frontend.

Features:
- Question answering
- Simple topic explanations
- MCQ quiz generation
- Text summarization
- Personalized learning paths

## Requirements

- Python 3.10+
- Gemini API key
- Internet connection for Gemini API
- Extra model dependencies are needed for the LaMini-Flan-T5 explanation feature.

## Setup

### 1. Create and activate a virtual environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` if you want to keep the values in a file.

The application reads `GEMINI_API_KEY` from the environment.

Linux/macOS:

```bash
export GEMINI_API_KEY="YOUR_KEY"
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
```

You can change the model with:

```bash
export GEMINI_MODEL="gemini-2.5-flash"
```

### 4. Run

```bash
uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

Swagger/OpenAPI:

http://127.0.0.1:8000/docs

## API endpoints

- POST `/qa`
- POST `/explain`
- POST `/quiz`
- POST `/summarize`
- POST `/learn/recommendations`

## Important note

The supplied project document describes Gemini 1.5 Pro and LaMini-Flan-T5-783M. This reconstructed runnable version keeps the same architecture and module responsibilities, but makes the Gemini model configurable through `GEMINI_MODEL`. The default is a currently configurable Gemini model name; set it to a model available to your API account if needed.

The LaMini-Flan-T5 model is downloaded the first time `/explain` is used and can require substantial disk space/RAM.
