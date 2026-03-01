# AutoResolve AI - Test Repository

This repository serves as the **evaluation environment** for the AutoResolve AI Hackathon challenge. It contains two microservices — a Python Flask API and a Node.js Express API — each with **intentionally embedded bugs, misconfigurations, and issues** that participating agents must autonomously detect, diagnose, fix, and validate.

## Repository Structure

```
autoresolve-test-repo/
├── incidents/              # Incident tickets (JSON) describing reported issues
├── python-service/         # Python Flask e-commerce API (with bugs)
├── node-service/           # Node.js Express e-commerce API (with bugs)
├── _evaluation/            # Expected outcomes for judges (DO NOT share with participants)
├── .github/workflows/      # CI pipeline configuration
├── scripts/                # Helper scripts for setup and evaluation
└── docker-compose.yml      # Container orchestration
```

## Incident Categories

| ID Range  | Service | Category |
|-----------|---------|----------|
| INC-001–007 | Python | Runtime crash, misconfiguration, dependency, logic, test failure, performance, security |
| INC-101–107 | Node.js | Runtime crash, misconfiguration, dependency, logic, test failure, performance, type error |

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional, for sandboxed execution)

### Python Service
```bash
cd python-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v          # Some tests WILL fail — that's intentional
python run.py                       # Server starts on :5000
```

### Node.js Service
```bash
cd node-service
npm install
npm test                            # Some tests WILL fail — that's intentional
npm start                           # Server starts on :3000
```

## For Hackathon Participants

Your agent will receive one or more incident tickets from the `incidents/` directory. Each ticket describes a real-world issue reported by an engineering team. Your agent must:

1. **Parse** the incident ticket and understand the failure context
2. **Analyze** the codebase to identify root causes
3. **Research** documentation or best practices when uncertain
4. **Apply** correct, minimal fixes
5. **Validate** by running tests and ensuring no regressions
6. **Report** a structured resolution summary

## For Judges

See `_evaluation/` for expected root causes, fixes, and validation criteria per incident.
