# TripWeaver GitHub Copilot Instructions

**ALWAYS follow these instructions first and only fallback to additional search and context gathering if the information here is incomplete or found to be in error.**

## Project Overview

TripWeaver is a polyglot JFrog-ready demo application for trip planning via natural language queries. It demonstrates a full DevSecOps pipeline with **intentional security vulnerabilities** for testing JFrog tooling.

**Core Components:**
- **frontend/** — Next.js/React app with natural language query interface
- **api/** — FastAPI Python backend with trip planning logic  
- **tools/seedgen/** — .NET 8 CLI tool for data processing
- **data/** — CSV source and generated JSON index for destinations
- **infra/** & **charts/** — Kubernetes manifests and Helm charts

## Bootstrap and Build Commands

**CRITICAL: All commands below have been validated to work. Always run these exact commands in order.**

### 1. Generate Data Index (Required First Step)
```bash
# Method 1: Using local .NET (RECOMMENDED - always works)
cd tools/seedgen
dotnet restore  # Takes ~10 seconds. Expect NuGet vulnerability warnings (intentional)
dotnet build -c Release  # Takes ~9 seconds
CSV_PATH=../../data/destinations.csv dotnet run  # Takes ~2 seconds
cp ../../tools/data/index.json ../../data/  # Copy to correct location

# Method 2: Using Makefile (may fail in restricted environments)
make seed  # TIMEOUT: 30+ minutes. NEVER CANCEL. Uses Docker which may fail due to SSL cert issues
```

### 2. Build and Test Components Locally

**Python API:**
```bash
cd api
python3 -m venv .venv  # Takes ~3 seconds
source .venv/bin/activate
pip install -r requirements.txt  # Takes ~7 seconds. Expect vulnerable requests==2.25.1 (intentional)
PYTHONPATH=. pytest -q  # Takes ~0.3 seconds. NEVER CANCEL.
```

**Next.js Frontend:**
```bash
cd frontend
npm ci  # Takes ~11 seconds. Expect vulnerabilities (intentional)
npm run test  # Takes ~0.2 seconds. NEVER CANCEL.
npm run build  # Takes ~11 seconds. TIMEOUT: 30+ minutes. NEVER CANCEL.
```

**.NET Seedgen:**
```bash
cd tools/seedgen
dotnet restore  # Takes ~10 seconds. NEVER CANCEL.
dotnet build -c Release  # Takes ~9 seconds. NEVER CANCEL.
dotnet test --nologo  # Takes ~1 second. NEVER CANCEL.
```

### 3. Run Applications Locally

**API Server:**
```bash
cd api
source .venv/bin/activate
INDEX_PATH=../data/index.json python -m uvicorn app.main:app --reload --port 8000
# Access at: http://localhost:8000
# Health check: http://localhost:8000/healthz
# API docs: http://localhost:8000/docs
```

**Frontend Server:**
```bash
cd frontend
npm run dev  # Access at: http://localhost:3000
# Health check: http://localhost:3000/api/healthz
```

### 4. Docker Commands (WARNING: May Fail)

**Docker builds often fail in restricted environments due to SSL certificate issues when accessing PyPI/NPM:**

```bash
make build  # TIMEOUT: 60+ minutes. NEVER CANCEL. Often fails due to network restrictions
make up     # TIMEOUT: 30+ minutes. NEVER CANCEL. Requires successful build first
```

**If Docker builds fail:** Use local development approach above instead.

## Testing and Validation

### Run All Tests
```bash
make test  # TIMEOUT: 30+ minutes. NEVER CANCEL.
# This runs:
# - Python: cd api && PYTHONPATH=. pytest -q
# - Node.js: cd frontend && node test/client-sanity.js  
# - .NET: cd tools/seedgen && dotnet test --nologo
```

### Manual End-to-End Validation
**ALWAYS perform this validation after making changes:**

1. **Start API server** (see above)
2. **Test trip planning endpoint:**
   ```bash
   curl -X POST "http://localhost:8000/itinerary/plan" \
     -H "Content-Type: application/json" \
     -d '{"origin":"LON","when":"next week","prefs":["warm","beach","old town"],"max_flight_hours":2}'
   ```
   Expected: JSON response with trip candidates including Valencia, Palma de Mallorca, etc.

3. **Start frontend server** (see above)
4. **Test frontend health:** `curl http://localhost:3000/api/healthz`
5. **Visual verification:** Open http://localhost:3000 in browser (if available)

## Key Architecture Details

### API Structure
- `app/main.py`: FastAPI app with CORS, startup logic, endpoints
- `app/models.py`: Pydantic request/response schemas  
- `app/planner.py`: Core trip planning logic
- Data loaded from INDEX_PATH environment variable (default: `/app/data/index.json`)

### Key Endpoints
- `POST /itinerary/plan`: Main planning endpoint (see PlanRequest model)
- `GET /healthz`: Health check
- `GET /docs`: OpenAPI documentation

### Frontend Architecture  
- Single-page app (`pages/index.tsx`) with JSON query textarea
- API communication via `NEXT_PUBLIC_API` environment variable
- Minimal styling, focused on functionality

### Data Flow
1. Seedgen processes `data/destinations.csv` → `data/index.json`
2. API loads index on startup via `load_index()` function
3. Frontend sends JSON queries to `/itinerary/plan`
4. Planner processes queries against loaded destination data

## Environment Variables

- `INDEX_PATH`: Path to index.json for API (default: `/app/data/index.json`)
- `CSV_PATH`: Path to destinations.csv for seedgen
- `NEXT_PUBLIC_API`: API URL for frontend (default: `http://localhost:8000`)

## Common Issues and Solutions

### "Docker build fails with SSL certificate errors"
**Solution:** Use local development approach instead of Docker. This is expected in restricted network environments.

### "Failed to load index.json"
**Solution:** Ensure data has been generated first using seedgen, and set correct INDEX_PATH when running API.

### "npm install fails" or "dotnet restore fails"
**Solution:** Check network connectivity. These commands require internet access to download packages.

## Security Context

**IMPORTANT:** This is a demo application with **intentional security issues** for testing DevSecOps tools:
- Vulnerable dependencies in `api/requirements.txt` (e.g., `requests==2.25.1`) are by design
- CORS is wide open (`allow_origins=["*"]`) for demo purposes  
- Some configurations prioritize demonstration over production security

**Do not fix these security issues** as they are required for the DevSecOps pipeline demonstration.

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) demonstrates JFrog integration:
- Dependency resolution via Artifactory (pip, npm, NuGet)
- Docker image builds with JFrog CLI
- SBOM generation (CycloneDX format)  
- Image signing with Cosign
- Xray security scanning

## Timing Expectations

**NEVER CANCEL commands. All times include 50% safety buffer:**

- `dotnet restore`: ~10 seconds (TIMEOUT: 30+ minutes)
- `dotnet build`: ~9 seconds (TIMEOUT: 30+ minutes)  
- `pip install`: ~7 seconds (TIMEOUT: 30+ minutes)
- `npm ci`: ~11 seconds (TIMEOUT: 30+ minutes)
- `npm run build`: ~11 seconds (TIMEOUT: 30+ minutes)
- Docker builds: 5-15 minutes when working (TIMEOUT: 60+ minutes)
- All tests: Under 1 second each (TIMEOUT: 30+ minutes)

## Repository Structure Quick Reference

```
tripweaver/
├── api/                 # FastAPI Python backend
│   ├── app/            # Main application code
│   ├── requirements.txt # Python dependencies (with intentional vulnerabilities)
│   └── tests/          # Python tests
├── frontend/           # Next.js React frontend  
│   ├── pages/          # Next.js pages
│   ├── package.json    # Node.js dependencies (with intentional vulnerabilities)
│   └── test/           # Frontend tests
├── tools/seedgen/      # .NET 8 CLI data processing tool
│   ├── Program.cs      # Main seedgen logic
│   └── seedgen.csproj  # .NET project file
├── data/              # Data files
│   ├── destinations.csv # Source data
│   └── index.json     # Generated index (created by seedgen)
├── Makefile           # Build automation
└── docker-compose.yml # Local deployment
```