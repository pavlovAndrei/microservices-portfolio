import os

import requests


class OrderClient:

    BASE_URL = os.getenv("ORDER_SERVICE_URL", "http://order_service:8000")

    @staticmethod
    def create_order():

        response = requests.post(
            f"{OrderClient.BASE_URL}/order"
        )

        return response