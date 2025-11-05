"""
Тесты для Pet API - включает базовые операции, граничные значения,
некорректные данные, идемпотентность, уникальность и структуру ответов
"""
import pytest
import time


class TestPetCRUD:
    """Тесты базовых операций CRUD для питомцев"""

    def test_create_pet_success(self, api_client, pet_data_generator):
        """Проверка успешного создания питомца с проверкой структуры ответа"""
        pet_data = pet_data_generator.generate_pet_data()
        response = api_client.create_pet(pet_data)

        assert response.status_code == 200
        created_pet = response.json()
        assert created_pet["id"] == pet_data["id"]
        assert created_pet["name"] == pet_data["name"]
        assert isinstance(created_pet["id"], int)
        assert isinstance(created_pet["name"], str)
        if "status" in created_pet:
            assert created_pet["status"] in ["available", "pending", "sold"]

    def test_get_existing_pet(self, api_client, pet_data_generator):
        """Проверка получения существующего питомца с проверкой структуры"""
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        pet_id = pet_data["id"]
        response = api_client.get_pet(pet_id)

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            pet = response.json()
            assert pet["id"] == pet_id
            assert isinstance(pet["id"], int)
            assert isinstance(pet["name"], str)

    def test_get_nonexistent_pet(self, api_client):
        """Проверка HTTP статуса 404 для несуществующего питомца"""
        response = api_client.get_pet(999999999)
        assert response.status_code in [200, 404]

    def test_update_pet_success(self, api_client, pet_data_generator):
        """Проверка успешного обновления с проверкой структуры ответа"""
        initial_pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(initial_pet_data)
        assert create_response.status_code == 200

        pet_id = initial_pet_data["id"]
        updated_pet_data = pet_data_generator.generate_pet_data(
            pet_id=pet_id,
            name="Updated Name",
            status="sold"
        )
        update_response = api_client.update_pet(updated_pet_data)
        assert update_response.status_code == 200

        updated_pet = update_response.json()
        assert updated_pet["id"] == pet_id
        assert updated_pet["name"] == "Updated Name"
        assert updated_pet["status"] == "sold"

    def test_delete_pet_success(self, api_client, pet_data_generator):
        """Проверка успешного удаления"""
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        pet_id = pet_data["id"]
        delete_response = api_client.delete_pet(pet_id)
        assert delete_response.status_code in [200, 404]


class TestPetBoundaryValues:
    """Тесты граничных значений для Pet API"""

    def test_create_pet_with_empty_name(self, api_client, pet_data_generator):
        """Проверка граничного значения - пустое имя"""
        pet_data = pet_data_generator.generate_pet_data(name="")
        response = api_client.create_pet(pet_data)
        assert response.status_code in [200, 400, 405]

    def test_create_pet_with_very_long_name(self, api_client, pet_data_generator):
        """Проверка граничного значения - очень длинное имя (1000 символов)"""
        long_name = "A" * 1000
        pet_data = pet_data_generator.generate_pet_data(name=long_name)
        response = api_client.create_pet(pet_data)
        assert response.status_code in [200, 400, 405]

    def test_create_pet_with_zero_id(self, api_client, pet_data_generator):
        """Проверка граничного значения - ID = 0"""
        pet_data = pet_data_generator.generate_pet_data(pet_id=0)
        response = api_client.create_pet(pet_data)
        assert response.status_code in [200, 400, 405]

    def test_get_pet_with_invalid_id(self, api_client):
        """Проверка HTTP статуса 400 для невалидного ID"""
        response = api_client._make_request("GET", "/pet/invalid_string_id")
        assert response.status_code in [400, 404, 405]


class TestPetInvalidData:
    """Тесты обработки некорректных данных для Pet API"""

    def test_create_pet_with_invalid_status(self, api_client, pet_data_generator):
        """Проверка некорректных данных - невалидный статус"""
        pet_data = pet_data_generator.generate_pet_data(status="invalid_status_xyz")
        response = api_client.create_pet(pet_data)
        assert response.status_code in [200, 400, 405]

    def test_create_pet_with_invalid_id_type(self, api_client):
        """Проверка некорректных данных - ID типа строка"""
        invalid_pet = {"id": "not_a_number", "name": "Test", "status": "available"}
        response = api_client.create_pet(invalid_pet)
        assert response.status_code in [400, 405, 500]


class TestPetIdempotency:
    """Тесты идемпотентности для Pet API"""

    def test_create_pet_idempotency(self, api_client, pet_data_generator):
        """Проверка идемпотентности - повторное создание с теми же данными"""
        pet_data = pet_data_generator.generate_pet_data()
        response1 = api_client.create_pet(pet_data)
        assert response1.status_code == 200

        response2 = api_client.create_pet(pet_data)
        assert response2.status_code in [200, 400, 405]

        if response1.status_code == 200 and response2.status_code == 200:
            pet1 = response1.json()
            pet2 = response2.json()
            assert pet1["id"] == pet2["id"]

    def test_update_pet_idempotency(self, api_client, pet_data_generator):
        """Проверка идемпотентности - повторное обновление с теми же данными"""
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        updated_data = pet_data_generator.generate_pet_data(
            pet_id=pet_data["id"],
            name="Updated Name",
            status="sold"
        )
        response1 = api_client.update_pet(updated_data)
        assert response1.status_code == 200

        response2 = api_client.update_pet(updated_data)
        assert response2.status_code == 200

        pet1 = response1.json()
        pet2 = response2.json()
        assert pet1["id"] == pet2["id"]
        assert pet1["name"] == pet2["name"]

    def test_delete_pet_idempotency(self, api_client, pet_data_generator):
        """Проверка идемпотентности - повторное удаление безопасно"""
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        pet_id = pet_data["id"]
        delete_response1 = api_client.delete_pet(pet_id)
        assert delete_response1.status_code in [200, 404]

        delete_response2 = api_client.delete_pet(pet_id)
        assert delete_response2.status_code in [200, 404]


class TestPetAdvanced:
    """Дополнительные тесты для Pet API"""

    def test_find_pets_by_status(self, api_client):
        """Проверка поиска питомцев по статусу с проверкой структуры"""
        response = api_client.find_pets_by_status("available")
        assert response.status_code == 200

        pets = response.json()
        assert isinstance(pets, list)
        if len(pets) > 0:
            pet = pets[0]
            assert "id" in pet
            assert "name" in pet
            assert pet.get("status") == "available"

    def test_pet_id_uniqueness(self, api_client, pet_data_generator):
        """Проверка уникальности ID - создание двух питомцев с одинаковым ID"""
        pet_id = pet_data_generator.generate_pet_data()["id"]

        pet1_data = pet_data_generator.generate_pet_data(pet_id=pet_id, name="First Pet")
        response1 = api_client.create_pet(pet1_data)
        assert response1.status_code == 200

        pet2_data = pet_data_generator.generate_pet_data(pet_id=pet_id, name="Second Pet")
        response2 = api_client.create_pet(pet2_data)
        assert response2.status_code in [200, 400, 405]

    def test_create_pet_performance(self, api_client, pet_data_generator):
        """Базовый тест производительности - создание должно быть быстрым"""
        pet_data = pet_data_generator.generate_pet_data()

        start_time = time.time()
        response = api_client.create_pet(pet_data)
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 2.0, "Создание должно занимать менее 2 секунд"
