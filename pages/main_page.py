from selenium.webdriver.common.by import By
from base.base_page import BasePage
import allure

class MainPage(BasePage):
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_logged_in_successfully(self):
        """验证是否成功登录（出现 Products 标题）"""
        return self.wait_for_visible(self.PRODUCTS_TITLE).is_displayed()

    @allure.step("退出登录")
    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)