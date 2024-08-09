import pytest
import allure
import requests
from conftest import reg_new_user_return_email_pass_del_this_user
from data import Constants, APIUserUrls, APIUserResponseTexts, UserTestData


@allure.epic('test_registration_user')
class TestRegistrationUser:

    @allure.title('Проверка регистрации уникального пользователя')
    @allure.description('Можно зарегистрировать пользователя c уникальными email, password и name')
    def test_registration_user_unique_user_data_true(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        assert response.status_code == 200 and response.json()["success"] == True

    @allure.title('Проверка регистрации пользователя, который уже был зарегистрирован')
    @allure.description('Если регистрировать пользователя с email, который уже есть, возвращается ошибка')
    def test_registration_user_user_already_exists_error_message(self, reg_new_user_return_email_pass_del_this_user):
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        same_email_pass = {"email": email_pass[0], "password": email_pass[1], "name": email_pass[2]}
        response = requests.post(Constants.MAIN_URL + APIUserUrls.REGISTRATION_USER_URL, data=same_email_pass)
        assert (response.status_code == 403 and response.json()["success"] == False
                and response.json()["message"] == APIUserResponseTexts.REGISTRATION_USER_ALREADY_EXISTS_ERROR)

    @allure.title('Проверка регистрации пользователя, при передачи в ручку не всех обязательных полей')
    @allure.description('Если одного из обязательных полей нет, запрос возвращает ошибку')
    @pytest.mark.parametrize('email, password, name',
                             [UserTestData.REGISTRATION_USER_WITHOUT_EMAIL_FIELD,
                              UserTestData.REGISTRATION_USER_WITHOUT_PASSWORD_FIELD,
                              UserTestData.REGISTRATION_USER_WITHOUT_NAME_FIELD])
    def test_registration_user_without_required_field_error_message(self, email, password, name):
        payload = {"email": email, "password": password, "firstName": name}
        response = requests.post(Constants.MAIN_URL + APIUserUrls.REGISTRATION_USER_URL, data=payload)
        assert (response.status_code == 403 and response.json()["success"] == False
                and response.json()["message"] == APIUserResponseTexts.REGISTRATION_USER_NO_REQUIRED_FIELD_ERROR)


@allure.epic('test_login_user')
class TestLoginUser:

    @allure.title('Проверка авторизации пользователя')
    @allure.description('Зарегистрированный пользователь может авторизоваться')
    def test_login_user_registered_user_data_true(self, reg_new_user_return_email_pass_del_this_user):
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": email_pass[0], "password": email_pass[1]}
        response = requests.post(Constants.MAIN_URL + APIUserUrls.LOGIN_USER_URL, data=payload)
        assert response.status_code == 200 and response.json()["success"] == True

    @allure.title('Проверка авторизации пользователя с неправильно указанным логином')
    @allure.description('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_login_user_wrong_email_error_message(self, reg_new_user_return_email_pass_del_this_user):
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": f'{email_pass[0]+'test1234'}', "password": email_pass[1]}
        response = requests.post(Constants.MAIN_URL + APIUserUrls.LOGIN_USER_URL, data=payload)
        assert (response.status_code == 401 and response.json()["success"] == False
                and response.json()["message"] == APIUserResponseTexts.LOGIN_USER_WRONG_LOGIN_PASS_ERROR)

    @allure.title('Проверка авторизации пользователя с неправильно указанным паролем')
    @allure.description('Если авторизоваться c неверным паролем, запрос возвращает ошибку')
    def test_login_user_wrong_pass_error_message(self, reg_new_user_return_email_pass_del_this_user):
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": email_pass[0], "password": f'{email_pass[1]+'12345'}'}
        response = requests.post(Constants.MAIN_URL + APIUserUrls.LOGIN_USER_URL, data=payload)
        assert (response.status_code == 401 and response.json()["success"] == False
                and response.json()["message"] == APIUserResponseTexts.LOGIN_USER_WRONG_LOGIN_PASS_ERROR)


@allure.epic('test_changing_user_data')
class TestChangingUserData:

    @allure.title('Проверка изменения данных авторизованного пользователя, email можно изменить')
    @allure.description('Авторизованный пользователь может изменить поле email')
    def test_changing_user_data_authorized_user_new_email_true(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": f'{email_pass[0]+'test1234'}', "password": email_pass[1], "name": email_pass[2]}
        response_patch = requests.patch(Constants.MAIN_URL + APIUserUrls.PATCH_USER_URL,
                                        headers={'Authorization': token}, data=payload)
        assert (response_patch.status_code == 200 and response.json()["success"] == True
                and response_patch.json()["user"]["email"] == f'{email_pass[0]+'test1234'}')

    @allure.title('Проверка изменения данных авторизованного пользователя, password можно изменить')
    @allure.description('Авторизованный пользователь может изменить поле password')
    def test_changing_user_data_authorized_user_new_password_true(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": email_pass[0], "password": f'{email_pass[1]+'1234'}', "name": email_pass[2]}
        response_patch = requests.patch(Constants.MAIN_URL + APIUserUrls.PATCH_USER_URL,
                                        headers={'Authorization': token}, data=payload)
        assert response_patch.status_code == 200 and response.json()["success"] == True

    @allure.title('Проверка изменения данных авторизованного пользователя, name можно изменить')
    @allure.description('Авторизованный пользователь может изменить поле name')
    def test_changing_user_data_authorized_user_new_name_true(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": email_pass[0], "password": email_pass[1], "name": f'{email_pass[2]+'test'}'}
        response_patch = requests.patch(Constants.MAIN_URL + APIUserUrls.PATCH_USER_URL,
                                        headers={'Authorization': token}, data=payload)
        assert (response_patch.status_code == 200 and response.json()["success"] == True
                and response_patch.json()["user"]["name"] == f'{email_pass[2]+'test'}')

    @allure.title('Проверка изменения данных неавторизованного пользователя')
    @allure.description('Неавторизованный пользователь не может изменить своих данных')
    def test_chang_user_data_not_auth_user_new_data_error_message(self, reg_new_user_return_email_pass_del_this_user):
        email_pass = reg_new_user_return_email_pass_del_this_user[1]
        payload = {"email": f'{email_pass[0]+'test1234'}', "password": f'{email_pass[1]+'1234'}',
                   "name": f'{email_pass[2]+'test'}'}
        response_patch = requests.patch(Constants.MAIN_URL + APIUserUrls.PATCH_USER_URL, data=payload)
        assert (response_patch.status_code == 401 and response_patch.json()["success"] == False
                and response_patch.json()["message"] == APIUserResponseTexts.CHANGING_USER_DATA_NOT_AUTH_USER_ERROR)
