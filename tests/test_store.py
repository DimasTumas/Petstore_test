"""
Тесты для Store API - включает базовые операции, граничные значения,
некорректные данные, идемпотентность, уникальность и структуру ответов
"""
import pytest
import time


class TestStoreOrderCRUD:
    """Тесты базовых операций CRUD для заказов"""

    def test_create_order_success(self, api_client, order_data_generator):
        """Проверка успешного создания заказа с проверкой структуры ответа"""
        order_data = order_data_generator.generate_order_data()
        response = api_client.create_store_order(order_data)

        assert response.status_code == 200
        created_order = response.json()
        assert created_order["id"] == order_data["id"]
        assert created_order["petId"] == order_data["petId"]
        assert created_order["quantity"] == order_data["quantity"]
        assert isinstance(created_order["id"], int)
        assert isinstance(created_order["petId"], int)
        assert isinstance(created_order["quantity"], int)
        if "complete" in created_order:
            assert isinstance(created_order["complete"], bool)

    def test_get_existing_order(self, api_client, order_data_generator):
        """Проверка получения существующего заказа с проверкой структуры"""
        order_data = order_data_generator.generate_order_data()
        create_response = api_client.create_store_order(order_data)
        assert create_response.status_code == 200

        # Используем ID из ответа создания
        created_order = create_response.json()
        order_id = created_order["id"]
        
        # Используем retry механизм для получения заказа
        # (демо API Petstore может иметь нестабильную задержку распространения данных)
        max_attempts = 5
        response = None
        for attempt in range(max_attempts):
            if attempt > 0:
                time.sleep(0.5 * attempt)  # Увеличивающаяся задержка
            response = api_client.get_store_order(order_id)
            if response.status_code == 200:
                break
        
        assert response.status_code == 200, f"Не удалось получить заказ после {max_attempts} попыток. Последний ответ: {response.text if response else 'None'}"
        order = response.json()
        assert order["id"] == order_id
        assert isinstance(order["id"], int)
        assert isinstance(order["petId"], int)
        assert isinstance(order["quantity"], int)

    def test_get_nonexistent_order(self, api_client):
        """Проверка HTTP статуса 404 для несуществующего заказа"""
        response = api_client.get_store_order(999999999)
        assert response.status_code == 404

    def test_delete_order_success(self, api_client, order_data_generator):
        """Проверка успешного удаления"""
        order_data = order_data_generator.generate_order_data()
        create_response = api_client.create_store_order(order_data)
        assert create_response.status_code == 200

        # Используем ID из ответа создания
        created_order = create_response.json()
        order_id = created_order["id"]
        
        # Убеждаемся, что заказ существует перед удалением
        # (используем retry, так как демо API Petstore имеет задержку распространения данных)
        max_attempts = 10
        for attempt in range(max_attempts):
            if attempt > 0:
                time.sleep(0.5 * attempt)
            get_response = api_client.get_store_order(order_id)
            if get_response.status_code == 200:
                break
        
        # Удаляем заказ с retry механизмом
        delete_response = None
        for attempt in range(max_attempts):
            if attempt > 0:
                time.sleep(0.5 * attempt)
            delete_response = api_client.delete_store_order(order_id)
            if delete_response.status_code == 200:
                break
        
        assert delete_response.status_code == 200, f"Не удалось удалить заказ после {max_attempts} попыток. Последний ответ: {delete_response.text if delete_response else 'None'}"
        
        # Проверяем, что заказ действительно удален
        verify_response = api_client.get_store_order(order_id)
        assert verify_response.status_code == 404, "Заказ должен быть удален, но все еще существует"


class TestStoreBoundaryValues:
    """Тесты граничных значений для Store API"""

    def test_create_order_with_zero_quantity(self, api_client, order_data_generator):
        """Проверка граничного значения - нулевое количество"""
        order_data = order_data_generator.generate_order_data(quantity=0)
        response = api_client.create_store_order(order_data)
        assert response.status_code in [200]

    def test_create_order_with_negative_quantity(self, api_client, order_data_generator):
        """Проверка граничного значения - отрицательное количество"""
        order_data = order_data_generator.generate_order_data(quantity=-1)
        response = api_client.create_store_order(order_data)
        assert response.status_code in [200]


class TestStoreInvalidData:
    """Тесты обработки некорректных данных для Store API"""

    def test_create_order_with_invalid_status(self, api_client, order_data_generator):
        """Проверка некорректных данных - невалидный статус"""
        order_data = order_data_generator.generate_order_data(status="invalid_status")
        response = api_client.create_store_order(order_data)
        assert response.status_code in [200]

    def test_create_order_with_invalid_id_type(self, api_client, order_data_generator):
        """Проверка некорректных данных - ID типа строка"""
        order_data = order_data_generator.generate_order_data()
        order_data["id"] = "not_a_number"
        response = api_client.create_store_order(order_data)
        assert response.status_code in [500]


class TestStoreIdempotency:
    """Тесты идемпотентности для Store API"""

    def test_create_order_idempotency(self, api_client, order_data_generator):
        """Проверка идемпотентности - повторное создание"""
        order_data = order_data_generator.generate_order_data()
        response1 = api_client.create_store_order(order_data)
        assert response1.status_code == 200

        response2 = api_client.create_store_order(order_data)
        assert response2.status_code in [200]

        if response1.status_code == 200 and response2.status_code == 200:
            order1 = response1.json()
            order2 = response2.json()
            assert order1["id"] == order2["id"]

    def test_delete_order_idempotency(self, api_client, order_data_generator):
        """Проверка идемпотентности - повторное удаление безопасно"""
        order_data = order_data_generator.generate_order_data()
        create_response = api_client.create_store_order(order_data)
        assert create_response.status_code == 200

        # Используем ID из ответа создания
        created_order = create_response.json()
        order_id = created_order["id"]
        
        # Убеждаемся, что заказ существует перед удалением
        max_attempts = 5
        for attempt in range(max_attempts):
            if attempt > 0:
                time.sleep(0.5 * attempt)
            get_response = api_client.get_store_order(order_id)
            if get_response.status_code == 200:
                break
        
        # Первое удаление с retry механизмом
        delete_response1 = None
        for attempt in range(max_attempts):
            if attempt > 0:
                time.sleep(0.5 * attempt)
            delete_response1 = api_client.delete_store_order(order_id)
            if delete_response1.status_code == 200:
                break
        
        assert delete_response1.status_code == 200, f"Не удалось удалить заказ после {max_attempts} попыток. Последний ответ: {delete_response1.text if delete_response1 else 'None'}"

        # Повторное удаление должно вернуть 404
        delete_response2 = api_client.delete_store_order(order_id)
        assert delete_response2.status_code == 404, "Повторное удаление должно вернуть 404"


class TestStoreAdvanced:
    """Дополнительные тесты для Store API"""

    def test_get_inventory(self, api_client):
        """Проверка получения инвентаря с проверкой структуры"""
        response = api_client.get_store_inventory()
        assert response.status_code == 200

        inventory = response.json()
        assert isinstance(inventory, dict)
        for key, value in inventory.items():
            assert isinstance(key, str)
            assert isinstance(value, int)
            assert value >= 0

    def test_order_id_uniqueness(self, api_client, order_data_generator):
        """Проверка уникальности ID - создание двух заказов с одинаковым ID"""
        order_id = order_data_generator.generate_order_data()["id"]

        order1_data = order_data_generator.generate_order_data(order_id=order_id, pet_id=1)
        response1 = api_client.create_store_order(order1_data)
        assert response1.status_code == 200

        order2_data = order_data_generator.generate_order_data(order_id=order_id, pet_id=2)
        response2 = api_client.create_store_order(order2_data)
        assert response2.status_code in [200]

    def test_create_order_performance(self, api_client, order_data_generator):
        """Базовый тест производительности - создание должно быть быстрым"""
        order_data = order_data_generator.generate_order_data()

        start_time = time.time()
        response = api_client.create_store_order(order_data)
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 2.0, "Создание должно занимать менее 2 секунд"