FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared module (needed by API)
COPY shared/ /app/shared/

# Copy API application code
COPY api/ /app/api/

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
