import requests
import random
import string
from api.courier_api import CourierAPI


class CourierHelper:

    @staticmethod
    def generate_random_string(length):

        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def register_new_courier_and_return_login_password():

        login_pass = []

        login = CourierHelper.generate_random_string(10)
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        return login_pass

    @staticmethod
    def delete_courier(login, password):

        courier_api = CourierAPI()

        # Получаем ID курьера для удаления
        response = courier_api.login_courier(login, password)
        if response.status_code == 200:
            courier_id = response.json()["id"]
            courier_api.delete_courier(courier_id)