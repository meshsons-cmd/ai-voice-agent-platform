# Portfolio Project Overview

## Engineering highlights
1. FastAPI REST endpoints and Pydantic validation.
2. Bounded LLM tool-calling loop.
3. Explicit tool allow-list and AST-based arithmetic evaluator (no `eval`).
4. SQLAlchemy persistence with SQLite default and PostgreSQL URL support.
5. OpenAI provider boundary plus shared tools exposed through MCP stdio.
6. Voice transcription and speech generation routes.
7. Docker Compose and GitHub Actions CI.

## Honest scope
This repository is a portfolio starter. It implements OpenAI tool calling; Gemini and Anthropic are not completed adapters. MCP is a local stdio server. Authentication and production hardening are not included.
