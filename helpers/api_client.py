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

    def get_store_order(self, order_id: int) -> requests.Response:
        return self._make_request("GET", f"/store/order/{order_id}")

    def create_store_order(self, order_data: Dict[str, Any]) -> requests.Response:
        return self._make_request(
            "POST",
            "/store/order",
            json=order_data,
            headers={"Content-Type": "application/json"}
        )
