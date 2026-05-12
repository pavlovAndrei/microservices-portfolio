from fastapi import FastAPI
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

import grpc
import json
import time

import payment_pb2
import payment_pb2_grpc


def create_topic():

    while True:

        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers='kafka:9092'
            )

            topic_list = [
                NewTopic(
                    name='order_created',
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
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

app = FastAPI()

create_topic()


@app.post("/order")
def create_order():

    channel = grpc.insecure_channel('payment_service:50051')

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

    producer.send("order_created", event)

    print("Event sent to Kafka", flush=True)

    return {
        "order_id": "123",
        "payment_status": response.status
    }