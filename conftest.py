import pytest
from helpers.api_client import PetstoreAPIClient
from helpers.data_generators import PetDataGenerator, OrderDataGenerator


@pytest.fixture(scope="function")
def api_client():
    yield PetstoreAPIClient()


@pytest.fixture(scope="function")
def pet_data_generator():
    yield PetDataGenerator


@pytest.fixture(scope="function")
def order_data_generator():
    yield OrderDataGenerator
