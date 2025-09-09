# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY . .

# Create data directory for database
RUN mkdir -p /app/data

# Set environment variables for the application
ENV DATABASE_PATH=/app/data/superheroes.db

# Expose port
EXPOSE 8000

# Command to check database and then run the application
CMD ["/bin/sh", "-c", "python check_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
