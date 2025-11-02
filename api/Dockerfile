# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code
COPY api/ .

# Copy agents directory from Agents/agents/
COPY Agents/agents/ ./

# Rename main2.0.py to main20.py (Python modules can't have dots)
RUN mv main2.0.py main20.py 2>/dev/null || true

# Create generated_assets directory
RUN mkdir -p generated_assets

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Run the application with gunicorn
# Note: Renamed main2.0.py to main20.py because Python module names can't have dots
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 300 --worker-class uvicorn.workers.UvicornWorker main20:app
