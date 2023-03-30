from requests import Session, Response
import allure
import json
import logging
from curlify import to_curl
from json import JSONDecodeError


def allure_logger(func):
    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]

        with allure.step(f"{method} {url}"):
            response: Response = func(*args, **kwargs)

            allure.attach(body=to_curl(response.request).encode('utf8'), name=f"Request: {response.status_code}",
                          attachment_type=allure.attachment_type.TEXT, extension='.txt')

            try:
                allure.attach(body=json.dumps(response.json(), indent=4), name=f"Response: {response.status_code}",
                              attachment_type=allure.attachment_type.JSON, extension='.json')
            except JSONDecodeError:
                allure.attach(body=response.text, name=f"Response: {response.status_code}",
                              attachment_type=allure.attachment_type.TEXT, extension='.txt')

            return response

    return wrapper


def request_logging(func):
    def wrapper(*args, **kwargs):
        response: Response = func(*args, **kwargs)
        logging.info(f"status code is {response.status_code} - {to_curl(response.request)}")

        return response

    return wrapper


class BaseSession(Session):
    def __init__(self, url):
        super(BaseSession, self).__init__()
        self.url = url

    @allure_logger
    @request_logging
    def request(self, method, url, **kwargs) -> Response:
        response = super().request(method, self.url + url, **kwargs)
        return response


regres = BaseSession('https://reqres.in/api')
demoshop = BaseSession('https://demowebshop.tricentis.com')