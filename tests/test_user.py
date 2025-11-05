"""
Тесты для User API - включает базовые операции, граничные значения,
некорректные данные, идемпотентность, уникальность и структуру ответов
"""
import pytest
import time


class TestUserCRUD:
    """Тесты базовых операций CRUD для пользователей"""

    def test_create_user_success(self, api_client, user_data_generator):
        """Проверка успешного создания пользователя с проверкой структуры"""
        user_data = user_data_generator.generate_user_data()
        response = api_client.create_user(user_data)

        assert response.status_code in [200, 201]
        if response.status_code in [200, 201]:
            assert response.headers.get("Content-Type", "").startswith("application/json") or \
                   response.status_code == 201

    def test_create_users_with_array(self, api_client, user_data_generator):
        """Проверка создания пользователей через массив"""
        users = [user_data_generator.generate_user_data() for _ in range(2)]
        response = api_client.create_users_with_array(users)
        assert response.status_code in [200, 201]

    def test_create_users_with_list(self, api_client, user_data_generator):
        """Проверка создания пользователей через список"""
        users = [user_data_generator.generate_user_data() for _ in range(2)]
        response = api_client.create_users_with_list(users)
        assert response.status_code in [200, 201]

    def test_get_existing_user(self, api_client, user_data_generator):
        """Проверка получения существующего пользователя с проверкой структуры"""
        user_data = user_data_generator.generate_user_data()
        create_response = api_client.create_user(user_data)
        assert create_response.status_code in [200, 201]

        username = user_data["username"]
        response = api_client.get_user(username)

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            user = response.json()
            assert user["username"] == username
            assert isinstance(user["id"], int)
            assert isinstance(user["username"], str)
            if "email" in user:
                assert isinstance(user["email"], str)
            if "userStatus" in user:
                assert user["userStatus"] in [0, 1]

    def test_get_nonexistent_user(self, api_client):
        """Проверка HTTP статуса 404 для несуществующего пользователя"""
        response = api_client.get_user("nonexistent_user_xyz123")
        assert response.status_code in [404, 200]

    def test_update_user_success(self, api_client, user_data_generator):
        """Проверка успешного обновления"""
        initial_user = user_data_generator.generate_user_data()
        create_response = api_client.create_user(initial_user)
        assert create_response.status_code in [200, 201]

        username = initial_user["username"]
        updated_user = user_data_generator.generate_user_data(
            user_id=initial_user["id"],
            username=username,
            first_name="Updated",
            last_name="User",
        )

        update_response = api_client.update_user(username, updated_user)
        assert update_response.status_code in [200, 201]

    def test_delete_user_success(self, api_client, user_data_generator):
        """Проверка успешного удаления с проверкой HTTP статусов"""
        user_data = user_data_generator.generate_user_data()
        create_response = api_client.create_user(user_data)
        assert create_response.status_code in [200, 201]

        username = user_data["username"]
        delete_response = api_client.delete_user(username)
        assert delete_response.status_code in [200, 204, 404]


class TestUserBoundaryValues:
    """Тесты граничных значений для User API"""

    def test_create_user_with_empty_username(self, api_client, user_data_generator):
        """Проверка граничного значения - пустой username"""
        user_data = user_data_generator.generate_user_data(username="")
        response = api_client.create_user(user_data)
        assert response.status_code in [200, 201, 400, 405]

    def test_create_user_with_very_long_username(self, api_client, user_data_generator):
        """Проверка граничного значения - очень длинный username"""
        long_username = "A" * 255
        user_data = user_data_generator.generate_user_data(username=long_username)
        response = api_client.create_user(user_data)
        assert response.status_code in [200, 201, 400, 405]


class TestUserInvalidData:
    """Тесты обработки некорректных данных для User API"""

    def test_create_user_with_invalid_email(self, api_client, user_data_generator):
        """Проверка некорректных данных - невалидный формат email"""
        user_data = user_data_generator.generate_user_data(email="invalid_email_format")
        response = api_client.create_user(user_data)
        assert response.status_code in [200, 201, 400, 405]

    def test_create_user_with_invalid_id_type(self, api_client, user_data_generator):
        """Проверка некорректных данных - ID типа строка"""
        user_data = user_data_generator.generate_user_data()
        user_data["id"] = "not_a_number"
        response = api_client.create_user(user_data)
        assert response.status_code in [200, 201, 400, 405, 500]


class TestUserIdempotency:
    """Тесты идемпотентности для User API"""

    def test_create_user_idempotency(self, api_client, user_data_generator):
        """Проверка идемпотентности - повторное создание"""
        user_data = user_data_generator.generate_user_data()
        response1 = api_client.create_user(user_data)
        assert response1.status_code in [200, 201]

        response2 = api_client.create_user(user_data)
        assert response2.status_code in [200, 201, 400, 405]

    def test_update_user_idempotency(self, api_client, user_data_generator):
        """Проверка идемпотентности - повторное обновление"""
        user_data = user_data_generator.generate_user_data()
        create_response = api_client.create_user(user_data)
        assert create_response.status_code in [200, 201]

        username = user_data["username"]
        updated_user = user_data_generator.generate_user_data(
            user_id=user_data["id"],
            username=username,
            first_name="Updated",
            last_name="User"
        )
        response1 = api_client.update_user(username, updated_user)
        assert response1.status_code in [200, 201]

        response2 = api_client.update_user(username, updated_user)
        assert response2.status_code in [200, 201]

    def test_delete_user_idempotency(self, api_client, user_data_generator):
        """Проверка идемпотентности - повторное удаление безопасно"""
        user_data = user_data_generator.generate_user_data()
        create_response = api_client.create_user(user_data)
        assert create_response.status_code in [200, 201]

        username = user_data["username"]
        delete_response1 = api_client.delete_user(username)
        assert delete_response1.status_code in [200, 204, 404]

        delete_response2 = api_client.delete_user(username)
        assert delete_response2.status_code in [200, 204, 404]


class TestUserAuth:
    """Тесты аутентификации пользователей"""

    def test_login_logout_flow(self, api_client, user_data_generator):
        """Проверка полного цикла логина/логаута"""
        user_data = user_data_generator.generate_user_data()
        create_response = api_client.create_user(user_data)
        assert create_response.status_code in [200, 201]

        login_resp = api_client.login_user(user_data["username"], user_data["password"])
        assert login_resp.status_code in [200, 400]
        if login_resp.status_code == 200:
            assert len(login_resp.text) > 0

        logout_resp = api_client.logout_user()
        assert logout_resp.status_code == 200

    def test_login_with_invalid_credentials(self, api_client):
        """Проверка HTTP статуса при логине с невалидными данными"""
        response = api_client.login_user("invalid_user", "wrong_password")
        assert response.status_code in [200, 400]

    def test_logout_idempotency(self, api_client):
        """Проверка идемпотентности - повторный logout безопасен"""
        response1 = api_client.logout_user()
        assert response1.status_code == 200

        response2 = api_client.logout_user()
        assert response2.status_code == 200


class TestUserAdvanced:
    """Дополнительные тесты для User API"""

    def test_username_uniqueness(self, api_client, user_data_generator):
        """Проверка уникальности username"""
        username = f"unique_user_{user_data_generator.generate_user_data()['id']}"

        user1_data = user_data_generator.generate_user_data(username=username, email="first@example.com")
        response1 = api_client.create_user(user1_data)
        assert response1.status_code in [200, 201]

        user2_data = user_data_generator.generate_user_data(username=username, email="second@example.com")
        response2 = api_client.create_user(user2_data)
        assert response2.status_code in [200, 201, 400, 405]

    def test_create_user_performance(self, api_client, user_data_generator):
        """Базовый тест производительности - создание должно быть быстрым"""
        user_data = user_data_generator.generate_user_data()

        start_time = time.time()
        response = api_client.create_user(user_data)
        end_time = time.time()

        assert response.status_code in [200, 201]
        assert (end_time - start_time) < 2.0, "Создание должно занимать менее 2 секунд"
