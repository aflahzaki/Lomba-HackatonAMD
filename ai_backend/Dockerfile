FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ai_backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ai_backend/app/ ./app/
COPY ai_backend/models/ ./models/

# Copy SIDATA SQL file into the container as fallback
# (volume mount in docker-compose is preferred at runtime)
COPY database/seed_sidata.sql /database/seed_sidata.sql

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
