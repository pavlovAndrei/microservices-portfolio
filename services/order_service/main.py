from fastapi import FastAPI
import grpc
from kafka import KafkaProducer

import payment_pb2
import payment_pb2_grpc

import json


app = FastAPI()


# Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def call_payment_service(order_id: str, amount: float):

    try:
        # gRPC channel
        channel = grpc.insecure_channel('localhost:50051')

        # gRPC client (stub)
        stub = payment_pb2_grpc.PaymentServiceStub(channel)

        # gRPC request
        response = stub.ProcessPayment(
            payment_pb2.PaymentRequest(
                order_id=order_id,
                amount=amount
            ),
            timeout=2
        )

        return response.status

    except Exception as e:
        return f"ERROR: {str(e)}"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/order")
def create_order():

    order_id = "123"
    amount = 100

    # call gRPC payment service
    payment_status = call_payment_service(order_id, amount)

    # event for Kafka
    event = {
        "order_id": order_id,
        "amount": amount,
        "payment_status": payment_status
    }

    # publish event
    producer.send("order_created", event)

    return {
        "order_id": order_id,
        "payment_status": payment_status
    }