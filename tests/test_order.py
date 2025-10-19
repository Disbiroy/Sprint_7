import pytest
import allure
from data.test_data import TestData


@allure.feature('Order API')
class TestOrder:

    @allure.title('Test order creation with different colors')
    @allure.description('Test order creation with BLACK, GREY, both colors and without color')
    @pytest.mark.parametrize('color', TestData.COLORS)
    def test_create_order_with_different_colors(self, color, order_api):
        # Готовим тестовые данные с помощью фикстуры или генератора
        order_data = TestData.generate_order_data(color=color)

        with allure.step(f'Create order with color: {color}'):
            response = order_api.create_order(**order_data)
            assert response.status_code == 201

            response_data = response.json()
            assert "track" in response_data
            assert isinstance(response_data["track"], int)

    @allure.title('Test get orders list')
    @allure.description('Test that orders list is returned correctly')
    def test_get_orders_list(self, order_api, created_order):
        # Фикстура created_order гарантирует, что есть хотя бы один заказ

        with allure.step('Get orders list'):
            response = order_api.get_orders_list()
            assert response.status_code == 200

            response_data = response.json()
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)
            assert len(response_data["orders"]) > 0  # Теперь гарантированно не пустой

            # Проверяем структуру первого заказа
            order = response_data["orders"][0]
            assert "id" in order
            assert isinstance(order["id"], int)
            assert "track" in order
            assert isinstance(order["track"], int)

    @allure.title('Test get order by track number')
    @allure.description('Test that order can be retrieved by track number')
    def test_get_order_by_track(self, order_api, created_order):
        order_track = created_order

        with allure.step('Get order by track number'):
            response = order_api.get_order_by_track(order_track)
            assert response.status_code == 200

            response_data = response.json()
            assert "order" in response_data
            order = response_data["order"]
            assert order["track"] == order_track
            assert "id" in order