FROM python:3.11-slim

WORKDIR /app

COPY services/payment_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/payment_service/ .

EXPOSE 50051

CMD ["python", "server.py"]
