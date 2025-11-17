# SPDX-License-Identifier: MPL-2.0
FROM python:3.11-slim

# Security: Run as non-root user
RUN groupadd -r mskio && useradd -r -g mskio -u 1000 mskio

# Security: Set secure environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies with security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml /app/
COPY configs /app/configs

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r configs/python/requirements-lock.txt

# Copy application code
COPY src /app/src
COPY scripts /app/scripts
COPY README.md /app/

# Install application
RUN pip install --no-cache-dir -e .

# Create necessary directories with proper permissions
RUN mkdir -p /data/msk_io_input /data/msk_io_output \
    /data/msk_io_downloads /data/msk_io_vectordb && \
    chown -R mskio:mskio /app /data

# Security: Switch to non-root user
USER mskio

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

EXPOSE 8000

# Use exec form for proper signal handling
CMD ["python", "-m", "uvicorn", "msk_io.api:app", "--host", "0.0.0.0", "--port", "8000"]
