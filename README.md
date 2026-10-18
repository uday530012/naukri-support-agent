# Naukri.com Domain Support Agent — CrewAI

An end-to-end AI-powered support agent for the **Naukri.com recruitment and HR domain**.

This project combines deterministic MOCK_LLM evaluation, RAG, CrewAI agents, LangChain session memory, guardrails, FastAPI, WebSocket communication, structured logging, AutoGen review, governance controls, and response caching.

---

## Project Overview

The Naukri Support Agent can:

- Answer recruitment and hiring-policy questions
- Retrieve information from a Naukri knowledge base
- Check specific job application status
- Calculate application escalation priority
- Maintain multi-turn conversation context
- Detect prompt injection attempts
- Mask phone numbers
- Block sensitive credential requests
- Return structured responses
- Expose REST and WebSocket APIs
- Log requests using JSONL
- Evaluate responses using deterministic MOCK_LLM tests
- Review CrewAI responses using AutoGen
- Classify request risk
- Enforce token/cost budgets
- Cache repeated responses

---

# Architecture

```text
                    USER
                      |
                      v
              +---------------+
              |   FastAPI API |
              +---------------+
                      |
                      v
              +---------------+
              |   Guardrails  |
              +---------------+
                      |
             +--------+--------+
             |                 |
             v                 v
       Policy Question    Application ID
             |                 |
             v                 v
       Retrieval Agent    Lookup Agent
             |                 |
             v                 v
          RAG KB          Application DB
             |                 |
             +--------+--------+
                      |
                      v
             Response Composer
                      |
                      v
                CrewAI Output
                      |
                      v
             AutoGen Review Team
                /           \
               v             v
           Reviewer      Final Editor
                \           /
                 +---------+
                      |
                      v
              Final Response
                      |
              +-------+-------+
              |               |
              v               v
           JSONL Log       Cache