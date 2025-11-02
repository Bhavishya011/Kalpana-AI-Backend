# Dockerfile
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for some Python packages (e.g., OpenCV)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This copies your api/ and Agents/ folders
COPY . .

# Expose the port that the application will listen on
EXPOSE 8080

# Define the command to run the application
# Use main.py which imports from api/main2.0.py
CMD ["python", "main.py"]