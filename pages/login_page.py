from selenium.webdriver.common.by import By
from base.base_page import BasePage
from pages.main_page import MainPage
import allure

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    URL = "https://www.saucedemo.com/"

    def open(self):
        self.go_to_url(self.URL)

    @allure.step("登录：用户名 {username}")
    def login(self, username, password):
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return MainPage(self.driver)

    @allure.step("尝试失败登录：用户名 {username}")
    def login_expect_fail(self, username, password):
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        error = self.wait_for_visible(self.ERROR_MESSAGE)
        return error.text