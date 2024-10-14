FROM python:3.12-slim

# Set environment variables to prevent Python from buffering output and to set up work directory
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and the application code to the container
COPY requirements.txt /app/
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (if your application runs on a specific port)
# EXPOSE 8080

# Command to run your Python program
CMD ["python", "src/main.py"]





## Including the test
# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port (if needed by your app)
EXPOSE 8000

# Run tests first, then the main program. The `&&` operator ensures tests must pass.
CMD ["sh", "-c", "python your_script.py --test && python your_script.py"]



## Multi-stage build
# Stage 1: Testing Stage
FROM python:3.12-slim  AS test-stage
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run tests in the test stage
RUN python your_script.py --test

# Stage 2: Production Stage
FROM python:3.12-slim AS production-stage
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1
COPY . .
EXPOSE 8000
CMD ["python", "your_script.py"]

