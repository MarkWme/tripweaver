# Alpine-based Python image for enhanced security
FROM python:3.11-alpine
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S appuser && adduser -S appuser -u 1001 -G appuser

# Copy dependency metadata first
COPY requirements.txt ./

# Install dependencies directly in Alpine
RUN set -eux; \
    echo "Python version: $(python --version)"; \
    echo "Pip version: $(pip --version)"; \
    echo "Installing dependencies from requirements.txt"; \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Security: Expose only necessary port
EXPOSE 8000

ENV NODE_ENV=production

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
