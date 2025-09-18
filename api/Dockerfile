FROM python:3.11-slim-bookworm AS base
WORKDIR /app

# Update system packages to ensure latest security patches
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# CVE-2025-6297 Mitigation: Create secure temp directory structure
RUN mkdir -p /app/secure-temp && \
    chmod 750 /app/secure-temp && \
    # Set up proper tmpfs mount point for secure temporary files
    mkdir -p /tmp/app-secure

# Copy dependency metadata first
COPY requirements.txt ./

# Install dependencies directly (platform-appropriate wheels will be selected automatically)
RUN set -eux; \
	echo "Python version: $(python --version)"; \
	echo "Pip version: $(pip --version)"; \
	echo "Installing dependencies from requirements.txt"; \
	pip install --no-cache-dir -r requirements.txt

COPY . /app

# CVE-2025-6297 Mitigation: Set environment variables for secure temp handling
ENV TMPDIR=/app/secure-temp
ENV TEMP=/app/secure-temp
ENV TMP=/app/secure-temp

# Add health check for disk monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
