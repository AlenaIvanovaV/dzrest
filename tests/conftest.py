from utils.base_session import BaseSession
import pytest
from selene.support.jquery_style_selectors import browser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
demoshop = BaseSession('https://demowebshop.tricentis.com')


@pytest.fixture(scope="function", autouse=True)
def chrome_browser():
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options)

    browser.config.driver = driver
    browser.config.base_url = 'https://demowebshop.tricentis.com'
    browser.config.window_height = 1080
    browser.config.window_width = 1920
    response = demoshop.post('/login', data={'Email': 'angel40995@inbox.ru', 'Password': 'qwerty'},
                       allow_redirects=False)
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')
    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie(
        {"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    return browser