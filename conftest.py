import pytest
import requests
from data import Constants, APIUserUrls
from generator import register_new_user_and_return_email_password


@pytest.fixture
def reg_new_user_return_email_pass_del_this_user():
    response, email_pass = register_new_user_and_return_email_password()
    yield response, email_pass
    token = response.json()['accessToken']
    requests.delete(Constants.MAIN_URL + APIUserUrls.DELETE_USER_URL, headers={'Authorization': token})
