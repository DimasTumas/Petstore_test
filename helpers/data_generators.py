import random
from typing import Dict, Any, List


class PetDataGenerator:
    NAMES = [
        "Buddy", "Max", "Charlie", "Cooper", "Rocky", "Bear", "Duke",
        "Luna", "Bella", "Lucy", "Daisy", "Molly", "Sadie", "Maggie"
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
