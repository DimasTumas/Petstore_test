import random
from typing import Dict, Any, List


class PetDataGenerator:
    NAMES = [
        "Барсик", "Пушок", "Рыжик", "Шарик", "Бобик", "Тузик", "Арчи",
        "Каспер", "Тишка", "Мурзик", "Соня", "Белка", "Лапка", "Звёздочка"
    ]

    CATEGORIES = [
        {"id": 1, "name": "Dogs"},
        {"id": 2, "name": "Cats"},
        {"id": 3, "name": "Birds"},
        {"id": 4, "name": "Fish"}
    ]

    TAGS = [
        {"id": 1, "name": "friendly"},
        {"id": 2, "name": "playful"},
        {"id": 3, "name": "loyal"},
        {"id": 4, "name": "active"},
        {"id": 5, "name": "calm"}
    ]

    STATUSES = ["available", "pending", "sold"]

    @classmethod
    def generate_pet_data(
        cls,
        pet_id: int = None,
        name: str = None,
        status: str = None,
        category: Dict[str, Any] = None,
        tags: List[Dict[str, Any]] = None,
        photo_urls: List[str] = None
    ) -> Dict[str, Any]:
        pet_id = pet_id or random.randint(100000, 999999)
        name = name or random.choice(cls.NAMES)
        status = status or random.choice(cls.STATUSES)
        category = category or random.choice(cls.CATEGORIES)
        tags = tags or random.sample(cls.TAGS, random.randint(1, 3))
        photo_urls = photo_urls or [f"https://example.com/photos/{name.lower()}.jpg"]

        return {
            "id": pet_id,
            "name": name,
            "status": status,
            "category": category,
            "tags": tags,
            "photoUrls": photo_urls
        }

    @classmethod
    def generate_minimal_pet_data(cls, pet_id: int = None) -> Dict[str, Any]:
        return cls.generate_pet_data(pet_id=pet_id)


class OrderDataGenerator:
    @classmethod
    def generate_order_data(
        cls,
        order_id: int = None,
        pet_id: int = None,
        quantity: int = None,
        status: str = None,
        complete: bool = None
    ) -> Dict[str, Any]:
        return {
            "id": order_id or random.randint(100000, 999999),
            "petId": pet_id or random.randint(1, 100),
            "quantity": quantity or random.randint(1, 10),
            "status": status or "placed",
            "complete": complete if complete is not None else False
        }


class UserDataGenerator:
    USER_STATUSES = [0, 1]

    FIRST_NAMES = [
        "Иван", "Петр", "Сергей", "Дмитрий", "Александр", "Николай", "Андрей",
        "Анна", "Ольга", "Мария", "Елена", "Татьяна", "Светлана", "Наталья"
    ]

    LAST_NAMES = [
        "Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Попов", "Соколов",
        "Волкова", "Семенова", "Лебедева", "Морозова", "Егорова", "Новикова", "Орлова"
    ]

    @classmethod
    def generate_user_data(
        cls,
        user_id: int = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        password: str = None,
        phone: str = None,
        user_status: int = None,
    ) -> Dict[str, Any]:
        user_id = user_id or random.randint(100000, 999999)
        first_name = first_name or random.choice(cls.FIRST_NAMES)
        last_name = last_name or random.choice(cls.LAST_NAMES)
        username = username or f"{first_name.lower()}_{last_name.lower()}_{random.randint(1000,9999)}"
        email = email or f"{username}@example.com"
        password = password or f"P@ssw0rd{random.randint(100,999)}"
        phone = phone or f"+7{random.randint(9000000000, 9999999999)}"
        user_status = user_status if user_status is not None else random.choice(cls.USER_STATUSES)

        return {
            "id": user_id,
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": password,
            "phone": phone,
            "userStatus": user_status,
        }
