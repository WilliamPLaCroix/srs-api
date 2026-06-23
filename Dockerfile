FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# create user EARLY (best practice)
RUN useradd -m appuser

# copy code with correct ownership upfront
COPY --chown=appuser:appuser . .

# upgrade packaging tools
RUN pip install --upgrade pip setuptools wheel

# install dependencies as root (acceptable for build step)
RUN pip install -e .

# switch user BEFORE runtime
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]