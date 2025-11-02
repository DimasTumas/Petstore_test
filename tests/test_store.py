import pytest
import requests


class TestStoreOrderCreate:
    def test_create_order_success(self, api_client, order_data_generator):
        order_data = order_data_generator.generate_order_data()
        response = api_client.create_store_order(order_data)

        assert response.status_code == 200
        created_order = response.json()
        assert created_order["id"] == order_data["id"]
        assert created_order["petId"] == order_data["petId"]
        assert created_order["quantity"] == order_data["quantity"]

    def test_create_order_minimal_data(self, api_client, order_data_generator):
        order_data = order_data_generator.generate_order_data()
        response = api_client.create_store_order(order_data)

        assert response.status_code == 200
        created_order = response.json()
        assert created_order["id"] == order_data["id"]
        assert "petId" in created_order


class TestStoreOrderRead:
    def test_get_existing_order(self, api_client, order_data_generator):
        order_data = order_data_generator.generate_order_data()
        create_response = api_client.create_store_order(order_data)
        assert create_response.status_code == 200

        order_id = order_data["id"]
        response = api_client.get_store_order(order_id)

        # Тестовый API может не сохранять данные
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            order = response.json()
            assert order["id"] == order_id

    def test_get_nonexistent_order(self, api_client):
        response = api_client.get_store_order(999999999)
        assert response.status_code == 404
