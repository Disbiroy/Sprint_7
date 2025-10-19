from dataclasses import dataclass
from typing import List


@dataclass
class ErrorMessages:
    DUPLICATE_COURIER = "Этот логин уже используется"
    INSUFFICIENT_DATA_CREATION = "Недостаточно данных для создания учетной записи"
    INSUFFICIENT_DATA_LOGIN = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"


@dataclass
class TestCouriers:
    WRONG_LOGIN = "wrong_login"
    WRONG_PASSWORD = "wrong_password"
    NONEXISTENT_USER = "nonexistent_user"
    NONEXISTENT_PASSWORD = "nonexistent_password"


class TestData:

    ORDER_DATA = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "ул. Тестовая, д. 1",
        "metroStation": 1,
        "phone": "+79999999999",
        "rentTime": 3,
        "deliveryDate": "2024-12-31",
        "comment": "Тестовый заказ",
        "color": ["BLACK"]
    }


    COLORS = [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ]


    @staticmethod
    def generate_order_data(**kwargs):

        order_data = TestData.ORDER_DATA.copy()
        order_data.update(kwargs)
        return order_data