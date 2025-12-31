# Worker Dockerfile

# Use slim Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/.hf_cache
ENV TRANSFORMERS_CACHE=/app/.hf_cache

# Set work directory
WORKDIR /worker

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY worker/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY worker/app ./app

# Copy shared module (needed by Worker)
COPY shared/ shared/

# Default command
CMD ["python", "-m", "app.main"]
