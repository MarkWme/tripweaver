FROM python:3.11-slim AS base
ARG ARTIFACTORY_PY_INDEX
ARG ARTIFACTORY_PY_EXTRA
ARG ARTIFACTORY_USER
ARG ARTIFACTORY_TOKEN
WORKDIR /app
COPY requirements.txt ./
# If an Artifactory index is provided, create a transient pip.conf, install, then remove it to avoid leaking creds.
RUN set -e; \
		if [ -n "$ARTIFACTORY_PY_INDEX" ]; then \
				echo "Using Artifactory Python index: $ARTIFACTORY_PY_INDEX"; \
				mkdir -p /root/.pip; \
				{ \
					echo "[global]"; \
					echo "index-url = ${ARTIFACTORY_PY_INDEX}"; \
					if [ -n "$ARTIFACTORY_PY_EXTRA" ]; then echo "extra-index-url = ${ARTIFACTORY_PY_EXTRA}"; fi; \
				} > /root/.pip/pip.conf; \
		fi; \
		pip install --no-cache-dir -r requirements.txt; \
		rm -f /root/.pip/pip.conf || true
COPY . /app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
