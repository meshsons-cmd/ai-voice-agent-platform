# AI Voice Agent Platform

A portfolio starter demonstrating a modular AI assistant backend.

## Features
- FastAPI REST API with typed Pydantic schemas
- OpenAI tool-calling agent with a bounded orchestration loop
- Allow-listed calculator and UTC-time tools
- SQLAlchemy conversation persistence (SQLite default; PostgreSQL supported by `DATABASE_URL`)
- Voice transcription and text-to-speech endpoints using OpenAI audio APIs
- MCP stdio server exposing shared tools
- Docker Compose and GitHub Actions CI

> This is a portfolio/reference implementation, not a production-hardened service. Authentication, authorization, rate limiting, managed secrets, observability, and deployment controls are future hardening tasks.

## Architecture
```text
Client -> FastAPI -> Agent service -> OpenAI tool-calling adapter
                         |          -> allow-listed tools
                         -> SQLAlchemy -> PostgreSQL / SQLite
MCP client -> stdio MCP server -> shared allow-listed tools
Voice client -> transcription / speech endpoints
```

## Setup
Python 3.11+ is required to run the application. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

## Docker
```bash
docker compose up --build
```

## Example
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is 125 multiplied by 8?"}'
```

## Voice API
- `POST /api/v1/voice/transcribe` — multipart audio upload
- `POST /api/v1/voice/speech` — JSON `{ "text": "Hello" }`, returns MP3 audio

## MCP
Run `python -m mcp_server.server` from the project root in an MCP-capable client configuration. The server uses stdio transport.

## Tests
Run `pytest`. Tests cover deterministic tools and API validation/health paths; they do not call external provider APIs.

## Provider scope
OpenAI tool calling and OpenAI voice endpoints are implemented. Gemini and Anthropic adapters are not claimed as implemented; the provider boundary is isolated for future extension. MCP is a local stdio server, not a hosted remote MCP service.

## Security checklist before production
Add authentication and per-user data ownership, rate limits, upload scanning and retention policy, managed secrets, strict CORS, structured monitoring, provider timeouts/retries, and spend controls.

MIT License. See `LICENSE`.
