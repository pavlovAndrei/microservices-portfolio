import pytest


BASE_URL = "http://order_service:8000"


@pytest.fixture
def base_url():

    return BASE_URL