from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class BasePage:
    """页面对象基类，封装通用操作"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_element(self, locator, timeout=10):
        """等待元素存在并返回"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.take_screenshot(f"element_not_found_{locator}")
            raise

    def click(self, locator):
        """点击元素（等待可点击）"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def input_text(self, locator, text):
        """输入文本（先清空）"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def wait_for_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def take_screenshot(self, name="screenshot"):
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)

    def go_to_url(self, url):
        self.driver.get(url)