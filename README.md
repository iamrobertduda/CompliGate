# CompliGate

A production-ready, offline-capable microservice for **PII (Personally Identifiable Information) anonymization**, built with [FastAPI](https://fastapi.tiangolo.com/), [Microsoft Presidio](https://microsoft.github.io/presidio/), and [spaCy](https://spacy.io/).

Designed for **air-gapped internal corporate networks** — no internet access required after the Docker image is built.

---

## Features

- 🔒 **PII Detection & Anonymization** — names, emails, IBANs, phone numbers, credit cards, and more
- 🚀 **Fast** — engines are loaded once at startup; requests are served in milliseconds
- 🛡️ **Secure** — runs as non-root user, no external calls at runtime
- 📦 **Offline-ready** — spaCy model is baked into the Docker image at build time
- 🐳 **Docker-first** — single `docker compose up` to run

## Quickstart

### Docker (recommended)

```bash
docker compose up --build
```

The service will be available at `http://localhost:8000`.

### Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000
```

## API

### `POST /sanitize`

Anonymizes PII in the provided text.

**Request:**

```json
{
  "text": "My name is John Doe and my email is john.doe@example.com. My IBAN is DE89370400440532013000."
}
```

**Response:**

```json
{
  "anonymized_text": "My name is <PERSON> and my email is <EMAIL_ADDRESS>. My IBAN is <IBAN_CODE>."
}
```

### `GET /health`

Returns service health status.

```json
{ "status": "healthy" }
```

### Interactive Docs

Once running, visit **http://localhost:8000/docs** for the auto-generated Swagger UI.

## Supported PII Entities

Presidio detects the following entity types out of the box:

| Entity | Example |
|---|---|
| `PERSON` | John Doe |
| `EMAIL_ADDRESS` | john@example.com |
| `PHONE_NUMBER` | +1-555-123-4567 |
| `IBAN_CODE` | DE89370400440532013000 |
| `CREDIT_CARD` | 4111-1111-1111-1111 |
| `IP_ADDRESS` | 192.168.1.1 |
| `US_SSN` | 123-45-6789 |
| `LOCATION` | New York |
| …and more | See [Presidio docs](https://microsoft.github.io/presidio/supported_entities/) |

## Project Structure

```
CompliGate/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Production container (Python 3.11 slim)
├── docker-compose.yml   # Orchestration with security constraints
├── .dockerignore        # Files excluded from Docker build
├── .gitignore           # Files excluded from Git
├── LICENSE              # MIT License
└── README.md            # This file
```

## Tech Stack

- **Python 3.11**
- **FastAPI** — async web framework
- **Microsoft Presidio** — PII analysis & anonymization
- **spaCy** (`en_core_web_sm`) — NLP engine for entity recognition
- **Uvicorn** — ASGI server

## License

This project is licensed under the [MIT License](LICENSE).
