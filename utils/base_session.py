from requests import Session, Response
import allure


class BaseSession(Session):
    def __init__(self, url):
        super(BaseSession, self).__init__()
        self.url = url

    def request(self, method, url, **kwargs) -> Response:
        with allure.step(f"{method} {url}"):
            return super().request(method, self.url + url, **kwargs)