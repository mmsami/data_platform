# Containerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    curl \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Rust - more explicit installation
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustc --version  # Verify Rust installation

# Copy requirements and install dependencies
COPY requirements.txt .
RUN . $HOME/.cargo/env && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY alembic.ini .
COPY migrations/ migrations/

# Set environment variables
ENV PYTHONPATH=/app

# Command to run migrations and start the application
CMD ["python", "-m", "src.main"]