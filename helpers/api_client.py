import requests
from typing import Dict, Any, Optional


class PetstoreAPIClient:
    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)

    def get_pet(self, pet_id: int) -> requests.Response:
        return self._make_request("GET", f"/pet/{pet_id}")

    def create_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        return self._make_request(
            "POST",
            "/pet",
            json=pet_data,
            headers={"Content-Type": "application/json"}
        )

    def update_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        return self._make_request(
            "PUT",
            "/pet",
            json=pet_data,
            headers={"Content-Type": "application/json"}
        )

    def delete_pet(self, pet_id: int) -> requests.Response:
        return self._make_request("DELETE", f"/pet/{pet_id}")

    def find_pets_by_status(self, status: str) -> requests.Response:
        """Поиск питомцев по статусу (available, pending, sold)"""
        return self._make_request("GET", "/pet/findByStatus", params={"status": status})

    def find_pets_by_tags(self, tags: list) -> requests.Response:
        """Поиск питомцев по тегам"""
        return self._make_request("GET", "/pet/findByTags", params={"tags": ",".join(tags)})

    def update_pet_with_form(self, pet_id: int, name: str = None, status: str = None) -> requests.Response:
        """Обновление питомца через форму"""
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        return self._make_request(
            "POST",
            f"/pet/{pet_id}",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    def upload_pet_image(self, pet_id: int, file_path: str = None, additional_metadata: str = None) -> requests.Response:
        """Загрузка изображения питомца"""
        files = None
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    files = {"file": f}
                    data = {}
                    if additional_metadata:
                        data["additionalMetadata"] = additional_metadata
                    return self._make_request("POST", f"/pet/{pet_id}/uploadImage", files=files, data=data)
            except FileNotFoundError:
                # Если файл не найден, отправляем без файла
                pass
        
        data = {}
        if additional_metadata:
            data["additionalMetadata"] = additional_metadata
        return self._make_request("POST", f"/pet/{pet_id}/uploadImage", files=files, data=data)

    # Store endpoints
    def get_store_inventory(self) -> requests.Response:
        """Получение инвентаря магазина"""
        return self._make_request("GET", "/store/inventory")

    def delete_store_order(self, order_id: int) -> requests.Response:
        """Удаление заказа"""
        return self._make_request("DELETE", f"/store/order/{order_id}")

    # User endpoints
    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        return self._make_request(
            "POST",
            "/user",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )

    def create_users_with_array(self, users: Any) -> requests.Response:
        return self._make_request(
            "POST",
            "/user/createWithArray",
            json=users,
            headers={"Content-Type": "application/json"}
        )

    def create_users_with_list(self, users: Any) -> requests.Response:
        return self._make_request(
            "POST",
            "/user/createWithList",
            json=users,
            headers={"Content-Type": "application/json"}
        )

    def get_user(self, username: str) -> requests.Response:
        return self._make_request("GET", f"/user/{username}")

    def update_user(self, username: str, user_data: Dict[str, Any]) -> requests.Response:
        return self._make_request(
            "PUT",
            f"/user/{username}",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )

    def delete_user(self, username: str) -> requests.Response:
        return self._make_request("DELETE", f"/user/{username}")

    def login_user(self, username: str, password: str) -> requests.Response:
        return self._make_request("GET", "/user/login", params={"username": username, "password": password})

    def logout_user(self) -> requests.Response:
        return self._make_request("GET", "/user/logout")

    def get_store_order(self, order_id: int) -> requests.Response:
        return self._make_request("GET", f"/store/order/{order_id}")

    def create_store_order(self, order_data: Dict[str, Any]) -> requests.Response:
        return self._make_request(
            "POST",
            "/store/order",
            json=order_data,
            headers={"Content-Type": "application/json"}
        )
