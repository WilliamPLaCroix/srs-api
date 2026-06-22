# Build command (from project root):
# docker build -t bookwurm .

FROM python:3.13-slim

# Prevent Python from writing .pyc files + ensure logs flush
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m appuser

# Copy app
COPY . .

RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# IMPORTANT: ensure src is importable
ENV PYTHONPATH=src

# Expose port (Render / local convenience)
EXPOSE 8000

# Start app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]