from fastapi import FastAPI
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

import grpc
import json
import os
import time

import payment_pb2
import payment_pb2_grpc

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC_ORDER = os.getenv("KAFKA_TOPIC_ORDER", "order_created")
PAYMENT_GRPC_TARGET = os.getenv("PAYMENT_GRPC_TARGET", "payment_service:50051")


def create_topic():

    while True:

        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
            )

            topic_list = [
                NewTopic(
                    name=KAFKA_TOPIC_ORDER,
                    num_partitions=1,
                    replication_factor=1
                )
            ]

            admin_client.create_topics(
                new_topics=topic_list,
                validate_only=False
            )

            print("Topic created", flush=True)

            return

        except TopicAlreadyExistsError:

            print("Topic already exists", flush=True)

            return

        except Exception as e:

            print(f"Kafka not ready yet: {e}", flush=True)

            time.sleep(5)


def get_kafka_producer():

    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

app = FastAPI()

create_topic()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/order")
def create_order():

    channel = grpc.insecure_channel(PAYMENT_GRPC_TARGET)

    stub = payment_pb2_grpc.PaymentServiceStub(channel)

    response = stub.ProcessPayment(
        payment_pb2.PaymentRequest(
            order_id="123"
        )
    )

    event = {
        "order_id": "123",
        "status": response.status
    }

    producer = get_kafka_producer()

    producer.send(KAFKA_TOPIC_ORDER, event)
    producer.flush()
    print("Event sent to Kafka", flush=True)

    return {
        "order_id": "123",
        "payment_status": response.status
    }