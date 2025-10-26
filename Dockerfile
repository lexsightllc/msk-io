FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml /app/
COPY src /app/src
COPY configs /app/configs

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r configs/python/requirements-lock.txt && \
    pip install --no-cache-dir -e .

COPY scripts /app/scripts
COPY README.md /app/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "msk_io.api:app", "--host", "0.0.0.0", "--port", "8000"]
