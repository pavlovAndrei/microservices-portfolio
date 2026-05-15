FROM python:3.11-slim

WORKDIR /app

COPY services/notification_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/notification_service/ .

CMD ["python", "main.py"]
