import json
import os
import time
import uuid

from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


def create_consumer(topic):

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id=f"test-{uuid.uuid4()}",
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    return consumer


def wait_for_event(topic, timeout=10):

    consumer = create_consumer(topic)

    end_time = time.time() + timeout

    while time.time() < end_time:

        batch = consumer.poll(timeout_ms=1000)

        for _, messages in batch.items():
            for message in messages:
                return message.value

    raise AssertionError(
        f"No events received from topic {topic}"
    )