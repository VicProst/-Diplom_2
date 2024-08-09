class Constants:
    MAIN_URL = 'https://stellarburgers.nomoreparties.site'

class APIUserUrls:
    REGISTRATION_USER_URL = '/api/auth/register'
    LOGIN_USER_URL = '/api/auth/login'
    DELETE_USER_URL = '/api/auth/user'
    PATCH_USER_URL = '/api/auth/user'

class APIUserResponseTexts:
    REGISTRATION_USER_ALREADY_EXISTS_ERROR = 'User already exists'
    REGISTRATION_USER_NO_REQUIRED_FIELD_ERROR = 'Email, password and name are required fields'
    LOGIN_USER_WRONG_LOGIN_PASS_ERROR = 'email or password are incorrect'
    CHANGING_USER_DATA_NOT_AUTH_USER_ERROR = 'You should be authorised'

class UserTestData:
    REGISTRATION_USER_WITHOUT_EMAIL_FIELD = ['', '123456', 'Victor']
    REGISTRATION_USER_WITHOUT_PASSWORD_FIELD = ['test765test432@@yandex.ru', '', 'Victor']
    REGISTRATION_USER_WITHOUT_NAME_FIELD = ['test765test432@@yandex.ru', '123456', '']

class APIOrderUrls:
    GET_INGREDIENTS_DATA_URL = '/api/ingredients'
    CREATING_ORDER_URL = '/api/orders'
    RECEIVING_USER_ORDERS_URL = '/api/orders'

class APIOrderResponseTexts:
    CREATING_ORDER_INVALID_HASH_ERROR = 'One or more ids provided are incorrect'
    CREATING_ORDER_NO_INGREDIENTS_ERROR = 'Ingredient ids must be provided'
    RECEIVING_USER_ORDERS_NOT_AUTH_USER_ERROR = 'You should be authorised'

class OrderTestData:
    CREATING_ORDER_ONE_INGREDIENT = ["61c0c5a71d1f82001bdaaa6d"]
    CREATING_ORDER_TWO_INGREDIENTS = ["61c0c5a71d1f82001bdaaa6d","61c0c5a71d1f82001bdaaa70"]
    CREATING_ORDER_FIVE_INGREDIENTS =["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f","61c0c5a71d1f82001bdaaa70",
                                      "61c0c5a71d1f82001bdaaa72", "61c0c5a71d1f82001bdaaa74"]
