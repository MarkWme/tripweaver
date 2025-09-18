FROM python:3.11-slim-bookworm AS base
WORKDIR /app

# Update system packages to ensure latest security patches
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependency metadata first
COPY requirements.txt ./

# Install dependencies directly (platform-appropriate wheels will be selected automatically)
RUN set -eux; \
	echo "Python version: $(python --version)"; \
	echo "Pip version: $(pip --version)"; \
	echo "Installing dependencies from requirements.txt"; \
	pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
