# Multi-stage build for Google Distroless Python
# Stage 1: Build dependencies using full Python image
FROM python:3.11-slim-bookworm AS builder
WORKDIR /app

# Update system packages to ensure latest security patches in builder stage
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependency metadata and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime using Google Distroless
FROM gcr.io/distroless/python3-debian12:nonroot
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/nonroot/.local

# Copy application code
COPY . /app

# Update PATH to include user-installed packages
ENV PATH="/home/nonroot/.local/bin:$PATH"
ENV PYTHONPATH="/home/nonroot/.local/lib/python3.11/site-packages"

# Security: Expose only necessary port
EXPOSE 8000

CMD ["/usr/bin/python3.11", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
