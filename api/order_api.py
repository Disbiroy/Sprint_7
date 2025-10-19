import requests


class OrderAPI:

    def __init__(self):
        self.base_url = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

    def create_order(self, first_name, last_name, address, metro_station, phone,
                     rent_time, delivery_date, comment, color=None):

        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment
        }

        if color:
            payload["color"] = color

        return requests.post(self.base_url, json=payload)

    def get_orders_list(self):

        return requests.get(self.base_url)

    def get_order_by_track(self, track):

        return requests.get(f"{self.base_url}/track", params={"t": track})