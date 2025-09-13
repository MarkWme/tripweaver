DEMO — TripWeaver

1) Seed data

   make seed

   This runs the .NET seedgen tool to convert data/destinations.csv → data/index.json.

2) Build images

   make build

   Builds three Docker images: api, frontend, and seedgen.

3) Bring up services

   make up

   Starts the API (http://localhost:8000) and frontend (http://localhost:3000). The frontend talks to the API and renders itinerary results.

4) Try an example

   curl -s -X POST "http://localhost:8000/itinerary/plan" -H "Content-Type: application/json" -d '{"origin":"LON","when":"next week","prefs":["warm","beach","old town"],"max_flight_hours":2}' | jq

   Or open http://localhost:3000 and enter a query.

5) SBOM and (stub) signing

   make sbom
   make sign

   SBOM artifacts are emitted to ./_sbom/. The signing step is a keyless stub that demonstrates the intended workflow.

Notes

- The backend exposes OpenAPI at http://localhost:8000/docs
- Health endpoints:
  - API: http://localhost:8000/healthz
  - Frontend: http://localhost:3000/healthz
