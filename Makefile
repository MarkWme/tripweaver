# Makefile for TripWeaver

IMAGE_API=tripweaver-api:local
IMAGE_FRONTEND=tripweaver-frontend:local
IMAGE_SEED=tripweaver-seedgen:local

.PHONY: seed build up test sbom sign clean

seed:
	docker build --target seed -t $(IMAGE_SEED) ./tools/seedgen
	docker run --rm -v $(PWD)/data:/app/data $(IMAGE_SEED)

build:
	docker build -t $(IMAGE_API) ./api
	docker build -t $(IMAGE_FRONTEND) ./frontend

up:
	docker-compose up --build -d
	@echo "API: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"

test:
	# Python tests
	cd api && PYTHONPATH=. pytest -q
	# Node tests (offline-friendly)
	cd frontend && node test/client-sanity.js
	# C# tests
	cd tools/seedgen && dotnet test --nologo

sbom:
	mkdir -p _sbom
	which syft >/dev/null 2>&1 || (echo "syft not found; please install" && exit 1)
	syft scan -o json -q $(IMAGE_API) > _sbom/api-sbom.json || true
	syft scan -o json -q $(IMAGE_FRONTEND) > _sbom/frontend-sbom.json || true
	syft scan -o json -q $(IMAGE_SEED) > _sbom/seed-sbom.json || true

sign:
	@echo "Signing images (will use real cosign only if COSIGN_KEY is set; otherwise creates stub signatures)"
	@mkdir -p _sbom
	@if ! command -v cosign >/dev/null 2>&1; then \
		echo "cosign not found; creating stub signatures"; \
		echo '{"signed":false}' > _sbom/api.sig.json; \
		echo '{"signed":false}' > _sbom/frontend.sig.json; \
		echo '{"signed":false}' > _sbom/seed.sig.json; \
	elif [ -n "$(COSIGN_KEY)" ]; then \
		echo "COSIGN_KEY provided; attempting to sign images with cosign using the provided key"; \
		cosign sign --key $(COSIGN_KEY) $(IMAGE_API) 2>/dev/null || echo '{"signed_by":"stub","image":"$(IMAGE_API)"}' > _sbom/api.sig.json; \
		cosign sign --key $(COSIGN_KEY) $(IMAGE_FRONTEND) 2>/dev/null || echo '{"signed_by":"stub","image":"$(IMAGE_FRONTEND)"}' > _sbom/frontend.sig.json; \
		cosign sign --key $(COSIGN_KEY) $(IMAGE_SEED) 2>/dev/null || echo '{"signed_by":"stub","image":"$(IMAGE_SEED)"}' > _sbom/seed.sig.json; \
	else \
		echo "cosign present but COSIGN_KEY not set; creating stub signatures (no --keyless attempted)"; \
		echo '{"signed":false}' > _sbom/api.sig.json; \
		echo '{"signed":false}' > _sbom/frontend.sig.json; \
		echo '{"signed":false}' > _sbom/seed.sig.json; \
	fi

clean:
	docker-compose down --rmi local --remove-orphans
	rm -rf _sbom
