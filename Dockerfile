# Multi-stage Dockerfile for Django application
# Demonstrates production-ready Docker practices

# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install minimal system dependencies and clean immediately
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    pip cache purge

# Stage 2: Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# No runtime dependencies needed for SQLite (remove postgresql-client)
# Copy application code
COPY . .

# Make sure scripts are executable
RUN chmod +x manage.py

# Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python manage.py check || exit 1

# Run migrations and start server
CMD python manage.py makemigrations --noinput && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput --clear && \
    python manage.py runserver 0.0.0.0:8000
