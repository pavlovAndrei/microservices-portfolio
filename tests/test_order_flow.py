import os

KAFKA_TOPIC_ORDER = os.getenv("KAFKA_TOPIC_ORDER", "order_created")
from tests.clients.order_client import OrderClient
from tests.utils.kafka_helper import wait_for_event


def test_order_event_created():

    response = OrderClient.create_order()

    assert response.status_code == 200

    event = wait_for_event(KAFKA_TOPIC_ORDER)

    assert event["status"] == "SUCCESS"