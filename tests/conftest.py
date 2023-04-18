from utils.base_session import BaseSession
import pytest
from selene.support.jquery_style_selectors import browser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dotenv import load_dotenv
import os
load_dotenv()

@pytest.fixture(scope='session')
def demoshop():
    return BaseSession(os.getenv("API_URL_DEMOSHOP"))

@pytest.fixture(scope="session", autouse=False)
def chrome_browser(demoshop):
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
    browser.config.base_url = "https://demowebshop.tricentis.com/"
    response = demoshop.post(
        "/login", json={"Email": os.getenv("LOGIN"), "Password": os.getenv("PASSWORD")}, allow_redirects=False)
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("Themes/DefaultClean/Content/images/logo.png")

    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    return browser