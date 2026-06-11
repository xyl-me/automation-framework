import requests
import allure

class BaseAPI:
    """API 请求基类，封装 HTTP 方法并附加 Allure 信息"""

    def __init__(self, base_url="https://petstore.swagger.io/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    @allure.step("{method} {endpoint}")
    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)
        return response

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)