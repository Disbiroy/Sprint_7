import pytest
import allure
from data.test_data import ErrorMessages, TestCouriers


@allure.feature('Courier API')
class TestCourier:

    @allure.title('Test successful courier creation')
    @allure.description('Test that courier can be created successfully')
    def test_create_courier_success(self, courier_api, courier_helper):
        login, password, first_name = courier_helper.register_new_courier_and_return_login_password()

        with allure.step('Check that courier was created'):
            response = courier_api.login_courier(login, password)
            assert response.status_code == 200

            # Проверяем тело ответа
            response_data = response.json()
            assert "id" in response_data
            assert isinstance(response_data["id"], int)
            assert response_data["id"] > 0

        # Удаление вынесено в фикстуру registered_courier

    @allure.title('Test duplicate courier creation')
    @allure.description('Test that cannot create two identical couriers')
    def test_create_duplicate_courier(self, registered_courier, courier_api):
        login, password, first_name = registered_courier

        with allure.step('Try to create duplicate courier'):
            response = courier_api.create_courier(login, password, first_name)
            assert response.status_code == 409

            # Проверяем тело ответа
            response_data = response.json()
            assert response_data["message"] == ErrorMessages.DUPLICATE_COURIER

    @allure.title('Test courier creation without required fields')
    @allure.description('Test that all required fields must be provided for courier creation')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field, courier_api, courier_helper):
        login = courier_helper.generate_random_string(10) if missing_field != 'login' else ""
        password = courier_helper.generate_random_string(10) if missing_field != 'password' else ""

        with allure.step(f'Try to create courier without {missing_field}'):
            response = courier_api.create_courier(login, password)
            assert response.status_code == 400

            # Проверяем тело ответа
            response_data = response.json()
            assert response_data["message"] == ErrorMessages.INSUFFICIENT_DATA_CREATION

    @allure.title('Test successful courier login')
    @allure.description('Test that courier can login successfully')
    def test_login_courier_success(self, registered_courier, courier_api):
        login, password, first_name = registered_courier

        with allure.step('Login with valid credentials'):
            response = courier_api.login_courier(login, password)
            assert response.status_code == 200

            # Проверяем тело ответа
            response_data = response.json()
            assert "id" in response_data
            assert isinstance(response_data["id"], int)
            assert response_data["id"] > 0

    @allure.title('Test courier login with wrong credentials')
    @allure.description('Test login with wrong login and password')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_courier_wrong_credentials(self, wrong_field, registered_courier, courier_api):
        login, password, first_name = registered_courier

        test_login = TestCouriers.WRONG_LOGIN if wrong_field == 'login' else login
        test_password = TestCouriers.WRONG_PASSWORD if wrong_field == 'password' else password

        with allure.step(f'Login with wrong {wrong_field}'):
            response = courier_api.login_courier(test_login, test_password)
            assert response.status_code == 404

            # Проверяем тело ответа
            response_data = response.json()
            assert response_data["message"] == ErrorMessages.ACCOUNT_NOT_FOUND

    @allure.title('Test courier login without required fields')
    @allure.description('Test login without required fields')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_missing_field(self, missing_field, courier_api, courier_helper):
        login = "" if missing_field == 'login' else courier_helper.generate_random_string(10)
        password = "" if missing_field == 'password' else courier_helper.generate_random_string(10)

        with allure.step(f'Login without {missing_field}'):
            response = courier_api.login_courier(login, password)
            assert response.status_code == 400

            # Проверяем тело ответа
            response_data = response.json()
            assert response_data["message"] == ErrorMessages.INSUFFICIENT_DATA_LOGIN

    @allure.title('Test login with non-existent user')
    @allure.description('Test login with non-existent user credentials')
    def test_login_nonexistent_user(self, courier_api):
        with allure.step('Login with non-existent credentials'):
            response = courier_api.login_courier(
                TestCouriers.NONEXISTENT_USER,
                TestCouriers.NONEXISTENT_PASSWORD
            )
            assert response.status_code == 404

            # Проверяем тело ответа
            response_data = response.json()
            assert response_data["message"] == ErrorMessages.ACCOUNT_NOT_FOUND