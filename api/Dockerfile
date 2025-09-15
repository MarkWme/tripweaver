FROM python:3.11-slim AS base
ARG ARTIFACTORY_PY_INDEX
ARG ARTIFACTORY_PY_EXTRA
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_TOKEN
WORKDIR /app
COPY requirements.txt ./
# Conditional install using Artifactory indices without writing a pip.conf (reduces syntax edge cases)
RUN set -euxo pipefail; \
	echo "Python version: $(python --version)"; \
	echo "Pip version: $(pip --version)"; \
	echo "Requirements contents:"; cat requirements.txt; \
	if [ -n "${ARTIFACTORY_PY_INDEX}" ]; then \
		BASE_INDEX="${ARTIFACTORY_PY_INDEX}"; \
		if [ -n "${ARTIFACTORY_USER}" ] && [ -n "${ARTIFACTORY_TOKEN}" ] && echo "$BASE_INDEX" | grep -q '://'; then \
			SCHEME=$(echo "$BASE_INDEX" | sed -E 's#^(https?)://.*#\1#'); \
			HOST_PATH=$(echo "$BASE_INDEX" | sed -E 's#^https?://##'); \
			AUTH_INDEX="${SCHEME}://${ARTIFACTORY_USER}:${ARTIFACTORY_TOKEN}@${HOST_PATH}"; \
			echo "Using authenticated Artifactory index"; \
			BASE_INDEX="$AUTH_INDEX"; \
		else \
			echo "Using Artifactory index without embedded creds (creds missing or already embedded)"; \
		fi; \
		if [ -n "${ARTIFACTORY_PY_EXTRA}" ]; then \
			PIP_INDEX_URL="$BASE_INDEX" PIP_EXTRA_INDEX_URL="${ARTIFACTORY_PY_EXTRA}" pip install -vv --no-cache-dir -r requirements.txt; \
		else \
			PIP_INDEX_URL="$BASE_INDEX" pip install -vv --no-cache-dir -r requirements.txt; \
		fi; \
	else \
		echo "No ARTIFACTORY_PY_INDEX provided, using default PyPI"; \
		pip install -vv --no-cache-dir -r requirements.txt; \
	fi
COPY . /app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
