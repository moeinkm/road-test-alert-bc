FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /code

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy dependency files first for better layer caching
COPY --chown=app:app Pipfile Pipfile.lock /code/

# Install dependencies
ARG ENVIRONMENT=local
ENV ENVIRONMENT=${ENVIRONMENT}

# Force virtual environment to be created in project directory
ENV PIPENV_VENV_IN_PROJECT=1

RUN if [ "$ENVIRONMENT" = "local" ]; then \
        # Local development: install from Pipfile for latest versions
        pipenv install --dev; \
    else \
        # Production: install from Pipfile.lock for reproducible builds
        pipenv install --deploy --ignore-pipfile; \
    fi

# Copy application code
COPY --chown=app:app . /code

# Make scripts executable
RUN chmod +x scripts/*.sh

# Set proper permissions
RUN chown -R app:app /code

# Switch to non-root user
USER app

# Set PATH to include virtual environment
ENV PATH="/code/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000

CMD ["bash", "-lc", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]
