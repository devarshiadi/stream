# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Set environment variables for Render
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Render uses
EXPOSE 10000

# Command to run the FastAPI app on Render's preferred port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
