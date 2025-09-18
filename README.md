# TripWeaver — polyglot JFrog-ready demo

## Overview

This repository is a minimal, production-shaped polyglot demo application designed to be wired into JFrog tooling later. It contains:

- **frontend/** — Next.js (React) frontend with a single natural-language query box
- **api/** — FastAPI Python backend exposing POST /itinerary/plan
- **tools/seedgen/** — .NET 8 CLI that reads data/destinations.csv and writes data/index.json
- **data/** — source CSV and generated JSON index
- **charts/** — Helm umbrella chart for deployment
- **infra/** — simple Kubernetes manifests for local kind testing

## Security Notice 🔐

**This repository includes security hardening measures to mitigate CVE-2025-8941** (libpam0g privilege escalation vulnerability). All containers run as non-root users and include PAM security configurations. See [SECURITY.md](./SECURITY.md) for detailed security information.

## Getting started (quick)

1. Generate data index:
   ```bash
   make seed
   ```
2. Build images:
   ```bash
   make build
   ```
3. Run locally with docker-compose:
   ```bash
   make up
   ```
4. Test (runs unit tests):
   ```bash
   make test
   ```
5. Generate SBOMs and (stub) sign images:
   ```bash
   make sbom && make sign
   ```

See `DEMO.md` for a step-by-step demo script.

## Security Validation

To validate security hardening measures:

```bash
./security/validate-security.sh
```

This script checks that all CVE-2025-8941 mitigation measures are properly implemented.

