# Use stable Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed to build wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to cache Docker layers
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy app code
COPY . .

# Default command
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.enableCORS=false"]
