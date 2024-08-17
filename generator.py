import allure
import requests
from data import Constants, APIUserUrls
from faker import Faker


faker = Faker()


@allure.step('Зарегистрировать нового пользователя и вернуть его email, password и name')
def register_new_user_and_return_email_password():
    email_pass = []
    email = 'test123' + faker.email()
    password = faker.password(length=6, special_chars=True, digits=True, upper_case=True, lower_case=True)
    name = faker.name()
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(Constants.MAIN_URL + APIUserUrls.REGISTRATION_USER_URL, data=payload)
    if response.status_code == 200:
        email_pass.append(email)
        email_pass.append(password)
        email_pass.append(name)
    return response, email_pass
