# AI Resume Analyzer

A Streamlit MVP that analyzes pasted resume text with OpenAI GPT and returns a validated, structured career assessment.

## Features

- Paste and submit resume text.
- Analyze the resume with OpenAI GPT.
- Generate a resume summary.
- Extract technical and soft skills with evidence and confidence.
- Assess experience level, strengths, and gaps.
- Recommend suitable job roles with fit reasoning.
- Identify missing skills and prioritized learning actions.
- Suggest actionable resume improvements.
- Keep secrets in `.env`, with exception handling and redacted logging.

The current MVP intentionally supports pasted text and in-memory Streamlit
session state. Uploads, accounts, consent workflows, persistence, background
jobs, reports, and job-feed integrations remain planned production extensions.

## Requirements

- Python 3.11+
- An OpenAI API key

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Add your key to `.env`:

```text
OPENAI_API_KEY=your-key-here
```

Do not commit `.env` or expose the key in source code.

## Run

```powershell
streamlit run app.py
```

Run the command from the repository root. Open the local URL shown by
Streamlit, paste the resume text, select **Submit Resume**, and then select
**Analyze Resume**.

## Test and quality checks

```powershell
python -m pytest
python -m ruff check src tests
python -m mypy src
```

The application uses a modular structure described in
[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md). [Architecture.md](Architecture.md)
describes the proposed production target and should not be read as a list of
currently implemented features.

## AI output safety

The AI response is constrained to strict Pydantic models and rejected when
malformed, incomplete, or oversized. Resume text is treated as untrusted
content in the prompt. Output is advisory and should be reviewed by the
candidate before use. Never commit `.env` or place a real API key in
`.env.example`.