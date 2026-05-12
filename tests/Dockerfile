FROM python:3.11

WORKDIR /app

COPY /tests /app/tests/
COPY /tests/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH=/app

CMD ["pytest", "-v"]