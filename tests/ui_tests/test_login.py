import pytest
import allure
from pages.login_page import LoginPage
from utils.data_helper import load_csv_data

def get_login_data():
    return load_csv_data("test_data/login_data.csv")

@allure.feature("登录模块")
@allure.story("用户登录验证")
class TestLogin:

    @pytest.mark.smoke
    @allure.title("正向登录：使用有效凭证")
    def test_valid_login(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        main_page = login_page.login("standard_user", "secret_sauce")
        assert main_page.is_logged_in_successfully()
        main_page.logout()

    @pytest.mark.parametrize("username,password,expected_error", [
        ("InvalidUser", "admin123", "Username and password do not match"),
        ("Admin", "wrongpass", "Username and password do not match"),
        ("", "admin123", "Username is required"),
        ("Admin", "", "Password is required")
    ])
    @allure.title("数据驱动登录失败场景：{username}/{password}")
    def test_invalid_login(self, driver, username, password, expected_error):
        login_page = LoginPage(driver)
        login_page.open()
        error_msg = login_page.login_expect_fail(username, password)
        # Swag Labs 的错误消息中会包含这些关键短语
        assert expected_error in error_msg

    @pytest.mark.parametrize("username,password,expected_result", get_login_data())
    @allure.title("CSV 数据驱动登录测试：{username}")
    def test_login_csv_driven(self, driver, username, password, expected_result):
        login_page = LoginPage(driver)
        login_page.open()
        if expected_result == "success":
            main_page = login_page.login(username, password)
            assert main_page.is_logged_in_successfully()
            main_page.logout()
        else:
            error_msg = login_page.login_expect_fail(username, password)
            # 根据实际错误消息判断：包含"Username"或"Password"或"locked out"
            assert ("Username" in error_msg or
                    "Password" in error_msg or
                    "locked out" in error_msg)