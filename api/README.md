API (FastAPI)

Getting started

cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

The API expects data/index.json at /app/data/index.json. For local development run `make seed` in the repo root to generate it.

Endpoints:
- POST /itinerary/plan — plan itineraries (see DEMO.md)
- GET /healthz — health check
- OpenAPI: /docs
