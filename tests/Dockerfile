FROM python:3.11-slim

WORKDIR /app

COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tests /app/tests
COPY framework /app/framework

ENV PYTHONPATH=/app

CMD ["pytest", "-v"]
