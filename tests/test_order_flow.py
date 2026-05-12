from kafka import KafkaConsumer
import json
import time
import requests



def create_test_consumer():

    consumer = KafkaConsumer(
        'order_created',
        bootstrap_servers="kafka:9092",
        group_id = 'test-group',
        auto_offset_reset = "earliest",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    return consumer

def test_create_order(base_url):

    response = requests.post(
        f"{base_url}/order"
    )

    assert response.status_code == 200


def test_order_event_created(base_url):

    consumer = create_test_consumer()

    time.sleep(3)

    response = requests.post(f"{base_url}/order")

    assert response.status_code == 200

    timeout = time.time() + 10
    events = []

    while time.time() < timeout:
        batch = consumer.poll(1000)

        for tp, messages in batch.items():
            for m in messages:
                events.append(m.value)

        if events:
            break

    assert len(events) > 0, "No Kafka events received"
    assert events[0]["status"] == "SUCCESS"
