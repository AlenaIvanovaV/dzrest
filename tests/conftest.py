import pytest
from selene.support.jquery_style_selectors import browser
from utils.base_session import BaseSession
from dotenv import load_dotenv
import os

load_dotenv()

demoshop = BaseSession('https://demowebshop.tricentis.com')


@pytest.fixture(scope='session')
def chrome_browser():
    browser.config.base_url = 'https://demowebshop.tricentis.com'
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    response = demoshop.post('/login', data={'Email': os.getenv('LOGIN'), 'Password': os.getenv('PASSWORD')},
                             allow_redirects=False)
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')
    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie(
        {"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    return browser