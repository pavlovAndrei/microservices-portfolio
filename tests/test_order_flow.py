from tests.clients.order_client import OrderClient
from tests.utils.kafka_helper import wait_for_event


def test_order_event_created():

    response = OrderClient.create_order()

    assert response.status_code == 200

    event = wait_for_event("order_created")

    assert event["status"] == "SUCCESS"