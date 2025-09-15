FROM python:3.11-slim AS base
WORKDIR /app
# Copy dependency metadata first
COPY requirements.txt ./
# Copy in wheelhouse (if supplied by build context) and install offline first
COPY wheelhouse /tmp/wheelhouse 2>/dev/null || true
RUN set -eux; \
	echo "Python version: $(python --version)"; \
	echo "Pip version: $(pip --version)"; \
	echo "Installing dependencies"; \
	if [ -d /tmp/wheelhouse ] && ls /tmp/wheelhouse/*.whl >/dev/null 2>&1; then \
		echo "Found pre-downloaded wheels, installing offline"; \
		pip install --no-cache-dir --no-index --find-links /tmp/wheelhouse -r requirements.txt; \
	else \
		echo "No wheelhouse provided; falling back to default index"; \
		pip install --no-cache-dir -r requirements.txt; \
	fi; \
	rm -rf /tmp/wheelhouse || true
COPY . /app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
