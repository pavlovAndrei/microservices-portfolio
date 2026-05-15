FROM python:3.11-slim

WORKDIR /app

COPY services/inventory_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/inventory_service/ .

CMD ["python", "main.py"]
