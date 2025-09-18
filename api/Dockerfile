FROM python:3.11-slim-bookworm AS base
WORKDIR /app

# Update system packages to ensure latest security patches
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# PAM Security Hardening for CVE-2025-8941 mitigation
# Create empty namespace.conf to prevent pam_namespace exploitation
RUN mkdir -p /etc/security && \
    echo "# Empty namespace.conf for CVE-2025-8941 mitigation" > /etc/security/namespace.conf && \
    chmod 644 /etc/security/namespace.conf && \
    chown root:root /etc/security/namespace.conf

# Create non-root user for security hardening (CVE-2025-8941 mitigation)
RUN groupadd -r tripweaver && useradd -r -g tripweaver -s /bin/false -c "TripWeaver API User" tripweaver

# Copy dependency metadata first
COPY requirements.txt ./

# Install dependencies directly (platform-appropriate wheels will be selected automatically)
RUN set -eux; \
	echo "Python version: $(python --version)"; \
	echo "Pip version: $(pip --version)"; \
	echo "Installing dependencies from requirements.txt"; \
	pip install --no-cache-dir -r requirements.txt

COPY . /app

# Set ownership and permissions for the application directory
RUN chown -R tripweaver:tripweaver /app && \
    chmod -R 755 /app

# Switch to non-root user
USER tripweaver

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
