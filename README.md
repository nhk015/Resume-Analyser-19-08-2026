# AI Resume Analyzer

## 1. Overview

AI Resume Analyzer is a Streamlit MVP that accepts pasted resume text and
returns a structured career assessment using OpenAI. The response is validated
with strict Pydantic models before it is displayed.

The current application is intentionally small and focused:

- Input is pasted text, not uploaded PDF or DOCX files.
- Results are held in Streamlit session state.
- Analysis calls are synchronous.
- An OpenAI API key is required for live analysis.

AI output is advisory. Users should verify every claim before using the result
in a resume, application, or career decision.

## 2. Features

- Paste, submit, and preview resume text.
- Enforce a configurable maximum resume length.
- Generate a concise resume summary.
- Extract technical and soft skills with evidence and confidence.
- Assess experience level, strengths, and gaps.
- Recommend job roles with fit scores and rationale.
- Identify missing or unevidenced skills.
- Generate prioritized learning suggestions.
- Generate prioritized resume improvements.
- Validate provider output against strict Pydantic schemas.
- Classify common OpenAI failures, including quota, authentication, timeout,
  connection, and rate-limit errors.
- Keep API credentials outside source code and avoid logging raw resume text.

## 3. Architecture

The project uses a small modular-monolith structure with ports and adapters:

```text
app.py
  -> presentation.streamlit_app
      -> application.services.AnalyzeResumeService
          -> domain.ports.AnalysisProvider
              -> infrastructure.ai.OpenAIResumeAnalyzer
                  -> OpenAI API
```

### Main boundaries

- `presentation`: Streamlit rendering, session state, and user interaction.
- `application`: Use-case orchestration and resume input validation.
- `domain`: Provider-independent models, protocols, and exceptions.
- `infrastructure.ai`: OpenAI SDK adapter, prompt construction, and response
  validation.
- `infrastructure.observability`: Central logging configuration and redaction.
- `container.py`: Dependency composition for the application.

The proposed production architecture in
[Architecture.md](Architecture.md) includes persistence, authentication,
background workers, uploads, reports, and job providers. Those features are
roadmap items and are not part of the current MVP.

## 4. Installation

### Prerequisites

- Python 3.11 or newer
- An OpenAI API key with available quota
- Git, if cloning the repository

Run all commands from the repository root, the directory containing
`pyproject.toml` and `app.py`.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation, either allow local scripts for your user or
run the commands through the virtual-environment executable directly:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

On Debian or Ubuntu, install the Python virtual-environment package if needed:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

### macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

If Python 3.11 is not installed, install it with Homebrew:

```bash
brew install python@3.11
```

## 5. Setup

Create a local environment file from the safe template.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
notepad .env
```

### Linux

```bash
cp .env.example .env
nano .env
```

### macOS

```bash
cp .env.example .env
open -a TextEdit .env
```

Set `OPENAI_API_KEY` to your own key in `.env`. Do not use the placeholder and
do not commit the file.

After changing environment variables while Streamlit is running, stop and
restart the application so its cached settings and dependencies are rebuilt.

## 6. Environment Variables

The application reads environment variables and, for local development, the
`.env` file in the current working directory. Environment variable names are
case-insensitive, but the uppercase names below are canonical.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes for live analysis | Empty | OpenAI API credential. Never commit or log it. |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | OpenAI chat model used for analysis. |
| `APP_ENV` | No | `development` | Application environment label. |
| `LOG_LEVEL` | No | `INFO` | One of `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. |
| `MAX_RESUME_CHARS` | No | `30000` | Maximum normalized resume length; valid range is 1,000 to 100,000. |
| `OPENAI_TIMEOUT_SECONDS` | No | `45` | Provider timeout in seconds; valid range is greater than 0 and at most 180. |

Example:

```dotenv
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
APP_ENV=development
LOG_LEVEL=INFO
MAX_RESUME_CHARS=30000
OPENAI_TIMEOUT_SECONDS=45
```

## 7. Running Application

Activate the virtual environment first, then run Streamlit from the repository
root.

### Windows PowerShell

```powershell
streamlit run app.py
```

### Linux and macOS

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit, usually
`http://localhost:8501`.

Workflow:

1. Paste the complete resume text.
2. Select **Submit Resume**.
3. Review the submitted text.
4. Select **Analyze Resume**.
5. Review the advisory results and supporting evidence.

Stop the development server with `Ctrl+C` in the terminal.

## 8. Running Tests

The test suite is deterministic. OpenAI calls are mocked, no real API key is
required, and tests do not depend on internet access.

### All tests

Windows PowerShell, Linux, and macOS:

```bash
python -m pytest
```

### Test categories

```bash
python -m pytest tests/unit
python -m pytest tests/integration
python -m pytest tests/negative
python -m pytest tests/validation
```

### Quality checks

```bash
python -m ruff check src tests app.py
python -m mypy src
```

The repository currently contains unit, integration, negative, validation, and
provider-adapter tests. Tests use temporary environment files and fake or
monkeypatched providers rather than the local `.env` credential.

## 9. Troubleshooting

### `OPENAI_API_KEY is not configured`

Check that:

1. `.env` exists in the repository root.
2. The variable is named exactly `OPENAI_API_KEY`.
3. The value is not the placeholder from `.env.example`.
4. Streamlit was started from the repository root.
5. Streamlit was restarted after changing `.env`.

Example:

```dotenv
OPENAI_API_KEY=sk-proj-your-key-here
```

Do not paste the key into an issue, terminal transcript, log, or chat.

### `429 insufficient_quota`

The key was accepted, but the OpenAI project has no available quota or credit.
Check the project billing and usage limits. Replacing the key alone will not
resolve an account quota problem.

### `The OpenAI API key was rejected`

Confirm that the key is active, belongs to the intended OpenAI project, and is
copied without extra quotes or spaces. If the key was exposed, revoke it and
create a replacement.

### `The AI provider could not be reached`

Check network connectivity, proxy settings, firewall rules, and the configured
timeout. The application does not provide an offline analysis mode.

### Invalid configuration errors

Check that:

- `LOG_LEVEL` is one of the supported values.
- `MAX_RESUME_CHARS` is between 1,000 and 100,000.
- `OPENAI_TIMEOUT_SECONDS` is greater than 0 and at most 180.

### The page shows stale state

Streamlit caches the dependency container and stores the current workflow in
session state. Refresh the page or restart Streamlit after configuration or
source changes.

## 10. Security Guidelines

- Revoke any API key that has been exposed in source control, logs, terminals,
  screenshots, or chat history.
- Keep real credentials only in local `.env` files or a managed secret store.
- Never commit `.env`; `.gitignore` is configured to exclude it.
- Keep `.env.example` limited to placeholders and non-secret defaults.
- Do not log API keys, authorization headers, raw resume text, or provider
  payloads.
- Treat resume text as sensitive personal data.
- Do not deploy this MVP publicly without authentication, rate limiting, quota
  controls, consent, retention, and deletion workflows.
- Review AI output before relying on it; the model can produce incorrect or
  unsupported recommendations.
- Pin and audit dependencies before production deployment.
- Use HTTPS and restrict access at the deployment boundary.
- Apply least privilege to API keys and use separate keys per environment.

## 11. Future Enhancements

Planned production capabilities include:

- PDF and DOCX upload with file type, size, malware, and text validation.
- Authentication, authorization, consent, retention, and deletion workflows.
- Durable persistence for resume metadata, analyses, and audit events.
- Background analysis jobs with retries, idempotency, and status tracking.
- Token budgets, usage metering, rate limiting, and cost controls.
- Evidence-linked findings and human review or correction workflows.
- Job-feed integrations and explainable role matching.
- Downloadable reports and controlled report sharing.
- Structured metrics, correlation IDs, alerting, and security monitoring.
- A production dependency lockfile, SBOM, and automated vulnerability scans.
- Migration from local SQLite-style storage to a server database when scale
  requires it.

## Related Documentation

- [Architecture](Architecture.md): proposed production architecture and
  boundaries.
- [Project Structure](PROJECT_STRUCTURE.md): current modules and roadmap areas.
- [Product Discovery](Product_discovery.md): product requirements and scope.
