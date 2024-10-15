FROM python:3.12-slim

# Environment variables to prevent Python from buffering output and to set up the virtual environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/opt/venv

# Create and activate the virtual environment
RUN python3 -m venv $VIRTUAL_ENV \
    && $VIRTUAL_ENV/bin/pip install --upgrade pip setuptools wheel

# Ensure venv is activated for all subsequent RUN commands
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Install system dependencies and clean up to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install code dependencies in virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy and set the entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy rest of the code
COPY . .

# Expose port and healthcheck
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8001/health || exit 1

# Set PYTHONPATH to point to the correct code directory
ENV APP_WORKDIR="/app"
ENV PYTHONPATH="${APP_WORKDIR}/"

# Command to run FastAPI using Uvicorn
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8001"]


