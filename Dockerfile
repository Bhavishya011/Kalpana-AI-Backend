# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set Python path to include Agents directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose port (Cloud Run will set PORT environment variable)
EXPOSE 8080

# Change to api directory and run the server
WORKDIR /app/api
CMD ["python", "main2.0.py"]
