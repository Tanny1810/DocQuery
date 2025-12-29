FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared module
COPY shared/ /app/shared/

# Copy API application code
COPY api/ /app/api/

# Copy entrypoint script
COPY api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set Python path
ENV PYTHONPATH=/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Entrypoint runs migrations, CMD runs app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
