FROM python:3.11-slim AS base
ARG ARTIFACTORY_PY_INDEX
ARG ARTIFACTORY_PY_EXTRA
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_TOKEN
WORKDIR /app
COPY requirements.txt ./
# Conditional install using Artifactory indices without writing a pip.conf (reduces syntax edge cases)
RUN set -e; \
	if [ -n "$ARTIFACTORY_PY_INDEX" ]; then \
		echo "Using Artifactory Python index: $ARTIFACTORY_PY_INDEX"; \
		if [ -n "$ARTIFACTORY_PY_EXTRA" ]; then \
			PIP_INDEX_URL="$ARTIFACTORY_PY_INDEX" PIP_EXTRA_INDEX_URL="$ARTIFACTORY_PY_EXTRA" pip install --no-cache-dir -r requirements.txt; \
		else \
			PIP_INDEX_URL="$ARTIFACTORY_PY_INDEX" pip install --no-cache-dir -r requirements.txt; \
		fi; \
	else \
		pip install --no-cache-dir -r requirements.txt; \
	fi
COPY . /app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
