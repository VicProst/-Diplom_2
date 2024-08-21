import pytest
import allure
import requests
from conftest import reg_new_user_return_email_pass_del_this_user
from data import Constants, APIOrderUrls, OrderTestData, APIOrderResponseTexts


@allure.epic('test_creating_order')
class TestCreatingOrder:

    @allure.title('Проверка создания заказа авторизованного пользователя с ингредиентами')
    @allure.description('Можно создать заказ авторизованным пользователем с 1, 2 и 5 ингридиентами')
    @pytest.mark.parametrize('ingredients',
                             [OrderTestData.CREATING_ORDER_ONE_INGREDIENT,
                              OrderTestData.CREATING_ORDER_TWO_INGREDIENTS,
                              OrderTestData.CREATING_ORDER_FIVE_INGREDIENTS])
    def test_creating_order_auth_user_valid_ingredients_true(self, ingredients,
                                                                   reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        payload = {"ingredients": ingredients}
        response_post = requests.post(Constants.MAIN_URL + APIOrderUrls.CREATING_ORDER_URL,
                                      headers={'Authorization': token}, data=payload)
        assert (response_post.status_code == 200 and response_post.json()["success"] == True
                and len(response_post.json()['order']['ingredients']) == len(ingredients))

    @allure.title('Проверка создания заказа неавторизованного пользователя с ингредиентами')
    @allure.description('Можно создать заказ неавторизованному пользователю с ингридиентами')
    def test_creating_order_not_auth_user_valid_ingredients_true(self):
        payload = {"ingredients": OrderTestData.CREATING_ORDER_ONE_INGREDIENT}
        response = requests.post(Constants.MAIN_URL + APIOrderUrls.CREATING_ORDER_URL, data=payload)
        assert (response.status_code == 200 and response.json()["success"] == True
                and "number" in response.json()['order'])

    @allure.title('Проверка создания заказа авторизованного пользователя без ингредиентов')
    @allure.description('Нельзя создать заказ авторизованным пользователем без ингридиентов')
    def test_creating_order_auth_user_no_ingredients_error_message(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        response_post = requests.post(Constants.MAIN_URL + APIOrderUrls.CREATING_ORDER_URL,
                                      headers={'Authorization': token})
        assert (response_post.status_code == 400 and response_post.json()["success"] == False
                and response_post.json()["message"] == APIOrderResponseTexts.CREATING_ORDER_NO_INGREDIENTS_ERROR)

    @allure.title('Проверка создания заказа неавторизованного пользователя без ингредиентов')
    @allure.description('Нельзя создать заказ неавторизованным пользователем без ингридиентов')
    def test_creating_order_not_auth_user_no_ingredients_error_message(self):
        response = requests.post(Constants.MAIN_URL + APIOrderUrls.CREATING_ORDER_URL)
        assert (response.status_code == 400 and response.json()["success"] == False
                and response.json()["message"] == APIOrderResponseTexts.CREATING_ORDER_NO_INGREDIENTS_ERROR)

    @allure.title('Проверка создания заказа авторизованного пользователя c неверным хешем ингредиентов')
    @allure.description('Нельзя создать заказ авторизованным пользователем c неверным хешем ингредиентов')
    def test_creating_order_auth_user_invalid_hash_error_message(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        payload = {"ingredients": ["123456a71d1f82001bdaaa6d"]}
        response_post = requests.post(Constants.MAIN_URL + APIOrderUrls.CREATING_ORDER_URL,
                                      headers={'Authorization': token}, data=payload)
        assert (response_post.status_code == 500 and response_post.json()["success"] == False
                and response_post.json()["message"] == APIOrderResponseTexts.CREATING_ORDER_INVALID_HASH_ERROR)

    @allure.title('Проверка создания заказа неавторизованного пользователя c неверным хешем ингредиентов')
    @allure.description('Нельзя создать заказ неавторизованным пользователем c неверным хешем ингредиентов')
    def test_creating_order_not_auth_user_invalid_hash_error_message(self):
        payload = {"ingredients": ["123456a71d1f82001bdaaa6d"]}
        response_post = requests.post(Constants.MAIN_URL + APIOrderUrls.CREATING_ORDER_URL, data=payload)
        assert (response_post.status_code == 500 and response_post.json()["success"] == False
                and response_post.json()["message"] == APIOrderResponseTexts.CREATING_ORDER_INVALID_HASH_ERROR)


@allure.epic('test_receiving_user_orders')
class TestReceivingUserOrders:

    @allure.title('Проверка получения заказа конкретного авторизованного пользователя')
    @allure.description('Можно получить заказ конкретного авторизованного пользователя')
    def test_receiving_user_orders_auth_user_true(self, reg_new_user_return_email_pass_del_this_user):
        response = reg_new_user_return_email_pass_del_this_user[0]
        token = response.json()['accessToken']
        response_get = requests.get(Constants.MAIN_URL + APIOrderUrls.RECEIVING_USER_ORDERS_URL,
                                      headers={'Authorization': token})
        assert (response_get.status_code == 200 and response_get.json()["success"] == True
                and "total" in response_get.json())

    @allure.title('Проверка получения заказа конкретного неавторизованного пользователя')
    @allure.description('Нельзя получить заказ конкретного неавторизованного пользователя')
    def test_receiving_user_orders_not_auth_user_error_message(self):
        response = requests.get(Constants.MAIN_URL + APIOrderUrls.RECEIVING_USER_ORDERS_URL)
        assert (response.status_code == 401 and response.json()["success"] == False
                and response.json()["message"] == APIOrderResponseTexts.RECEIVING_USER_ORDERS_NOT_AUTH_USER_ERROR)
