import pytest
import allure
from api.order_api import OrderAPI
from data.test_data import TestData


@allure.feature('Order API')
class TestOrder:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.order_api = OrderAPI()

    @allure.title('Test order creation with different colors')
    @allure.description('Test order creation with BLACK, GREY, both colors and without color')
    @pytest.mark.parametrize('color', TestData.COLORS)
    def test_create_order_with_different_colors(self, color):

        order_data = TestData.ORDER_DATA.copy()

        with allure.step(f'Create order with color: {color}'):
            response = self.order_api.create_order(
                first_name=order_data["firstName"],
                last_name=order_data["lastName"],
                address=order_data["address"],
                metro_station=order_data["metroStation"],
                phone=order_data["phone"],
                rent_time=order_data["rentTime"],
                delivery_date=order_data["deliveryDate"],
                comment=order_data["comment"],
                color=color
            )

            assert response.status_code == 201
            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)

    @allure.title('Test get orders list')
    @allure.description('Test that orders list is returned correctly')
    def test_get_orders_list(self):

        with allure.step('Get orders list'):
            response = self.order_api.get_orders_list()
            assert response.status_code == 200

            response_data = response.json()
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)

            # Проверяем, что список не пустой (если есть заказы)
            if len(response_data["orders"]) > 0:
                order = response_data["orders"][0]
                assert "id" in order
                assert "track" in order