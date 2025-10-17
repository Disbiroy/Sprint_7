import pytest
import allure
from api.courier_api import CourierAPI
from helpers.courier_helpers import CourierHelper


@allure.feature('Courier API')
class TestCourier:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.courier_api = CourierAPI()
        self.courier_helper = CourierHelper()

    @allure.title('Test successful courier creation')
    @allure.description('Test that courier can be created successfully')
    def test_create_courier_success(self):

        login, password, first_name = self.courier_helper.register_new_courier_and_return_login_password()

        with allure.step('Check that courier was created'):
            response = self.courier_api.login_courier(login, password)
            assert response.status_code == 200

        # Удаляем курьера после теста
        self.courier_helper.delete_courier(login, password)

    @allure.title('Test duplicate courier creation')
    @allure.description('Test that cannot create two identical couriers')
    def test_create_duplicate_courier(self):

        login, password, first_name = self.courier_helper.register_new_courier_and_return_login_password()

        with allure.step('Try to create duplicate courier'):
            response = self.courier_api.create_courier(login, password, first_name)
            assert response.status_code == 409
            assert "Этот логин уже используется" in response.text

        self.courier_helper.delete_courier(login, password)

    @allure.title('Test courier creation without required fields')
    @allure.description('Test that all required fields must be provided for courier creation')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field):

        login = self.courier_helper.generate_random_string(10) if missing_field != 'login' else ""
        password = self.courier_helper.generate_random_string(10) if missing_field != 'password' else ""

        with allure.step(f'Try to create courier without {missing_field}'):
            response = self.courier_api.create_courier(login, password)
            assert response.status_code == 400
            assert "Недостаточно данных для создания учетной записи" in response.text

    @allure.title('Test successful courier login')
    @allure.description('Test that courier can login successfully')
    def test_login_courier_success(self):

        login, password, first_name = self.courier_helper.register_new_courier_and_return_login_password()

        with allure.step('Login with valid credentials'):
            response = self.courier_api.login_courier(login, password)
            assert response.status_code == 200
            assert "id" in response.json()

        self.courier_helper.delete_courier(login, password)

    @allure.title('Test courier login with wrong credentials')
    @allure.description('Test login with wrong login and password')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_courier_wrong_credentials(self, wrong_field):

        login, password, first_name = self.courier_helper.register_new_courier_and_return_login_password()

        test_login = "wrong_login" if wrong_field == 'login' else login
        test_password = "wrong_password" if wrong_field == 'password' else password

        with allure.step(f'Login with wrong {wrong_field}'):
            response = self.courier_api.login_courier(test_login, test_password)
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.text

        self.courier_helper.delete_courier(login, password)

    @allure.title('Test courier login without required fields')
    @allure.description('Test login without required fields')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_missing_field(self, missing_field):

        login = "" if missing_field == 'login' else self.courier_helper.generate_random_string(10)
        password = "" if missing_field == 'password' else self.courier_helper.generate_random_string(10)

        with allure.step(f'Login without {missing_field}'):
            response = self.courier_api.login_courier(login, password)
            assert response.status_code == 400
            assert "Недостаточно данных для входа" in response.text

    @allure.title('Test login with non-existent user')
    @allure.description('Test login with non-existent user credentials')
    def test_login_nonexistent_user(self):
        
        with allure.step('Login with non-existent credentials'):
            response = self.courier_api.login_courier("nonexistent_user", "nonexistent_password")
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.text