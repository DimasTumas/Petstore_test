import pytest
import requests


class TestPetCreate:
    def test_create_pet_success(self, api_client, pet_data_generator):
        pet_data = pet_data_generator.generate_pet_data()
        response = api_client.create_pet(pet_data)

        assert response.status_code == 200
        created_pet = response.json()
        assert created_pet["id"] == pet_data["id"]
        assert created_pet["name"] == pet_data["name"]

    def test_create_pet_minimal_data(self, api_client, pet_data_generator):
        pet_data = pet_data_generator.generate_minimal_pet_data()
        response = api_client.create_pet(pet_data)

        assert response.status_code == 200
        created_pet = response.json()
        assert created_pet["id"] == pet_data["id"]
        assert "name" in created_pet

    def test_create_pet_with_all_fields(self, api_client, pet_data_generator):
        pet_data = pet_data_generator.generate_pet_data()
        response = api_client.create_pet(pet_data)

        assert response.status_code == 200
        created_pet = response.json()
        assert created_pet["id"] == pet_data["id"]
        assert created_pet["category"] == pet_data["category"]
        assert len(created_pet["tags"]) == len(pet_data["tags"])


class TestPetRead:
    def test_get_existing_pet(self, api_client, pet_data_generator):
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        pet_id = pet_data["id"]
        response = api_client.get_pet(pet_id)

        # Тестовый API может не сохранять данные
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            pet = response.json()
            assert pet["id"] == pet_id

    def test_get_nonexistent_pet(self, api_client):
        response = api_client.get_pet(999999999)
        assert response.status_code in [200, 404]

    def test_get_pet_with_invalid_id(self, api_client):
        response = api_client.get_pet("invalid_id")
        assert response.status_code in [400, 404]


class TestPetUpdate:
    def test_update_pet_success(self, api_client, pet_data_generator):
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

    def test_update_nonexistent_pet(self, api_client, pet_data_generator):
        non_existent_pet = pet_data_generator.generate_pet_data(pet_id=999999999)
        response = api_client.update_pet(non_existent_pet)
        assert response.status_code in [200, 404]


class TestPetDelete:
    def test_delete_pet_success(self, api_client, pet_data_generator):
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        pet_id = pet_data["id"]
        delete_response = api_client.delete_pet(pet_id)
        assert delete_response.status_code in [200, 404]

    def test_delete_nonexistent_pet(self, api_client):
        response = api_client.delete_pet(999999999)
        assert response.status_code in [200, 404]

    def test_delete_pet_with_invalid_id(self, api_client):
        response = api_client.delete_pet(-1)
        assert response.status_code in [200, 400, 404]


class TestPetWorkflows:
    def test_full_crud_workflow(self, api_client, pet_data_generator):
        # Создание
        pet_data = pet_data_generator.generate_pet_data()
        create_response = api_client.create_pet(pet_data)
        assert create_response.status_code == 200

        pet_id = pet_data["id"]
        created_pet = create_response.json()
        assert created_pet["name"] == pet_data["name"]

        # Обновление
        updated_data = pet_data_generator.generate_pet_data(
            pet_id=pet_id,
            name="Updated Name",
            status="pending"
        )
        update_response = api_client.update_pet(updated_data)
        assert update_response.status_code == 200

        updated_pet = update_response.json()
        assert updated_pet["name"] == "Updated Name"

        # Удаление
        delete_response = api_client.delete_pet(pet_id)
        assert delete_response.status_code == 200

    def test_multiple_pets_operations(self, api_client, pet_data_generator):
        pets = []
        for _ in range(3):
            pet_data = pet_data_generator.generate_pet_data()
            create_response = api_client.create_pet(pet_data)
            assert create_response.status_code == 200
            pets.append(pet_data)

        for pet_data in pets:
            delete_response = api_client.delete_pet(pet_data["id"])
            assert delete_response.status_code in [200, 404]
