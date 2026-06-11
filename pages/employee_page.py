from selenium.webdriver.common.by import By
from base.base_page import BasePage
import allure

class EmployeePage(BasePage):
    # 新增员工
    ADD_BUTTON = (By.XPATH, "//button[contains(@class, 'oxd-button') and text()=' Add ']")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMPLOYEE_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/ancestor::div[1]/following-sibling::div/input")
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit' and text()=' Save ']")
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class, 'oxd-toast--success')]")

    # 搜索员工
    SEARCH_NAME_INPUT = (By.XPATH, "//label[text()='Employee Name']/ancestor::div[1]/following-sibling::div//input")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit' and text()=' Search ']")
    SEARCH_RESULT_NAME = (By.XPATH, "//div[@class='oxd-table-card']//div[contains(@class, 'employee-name')]")

    @allure.step("新增员工：{first_name} {last_name}")
    def add_employee(self, first_name, last_name, employee_id=None):
        self.click(self.ADD_BUTTON)
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        if employee_id:
            emp_id_input = self.find_element(self.EMPLOYEE_ID_INPUT)
            emp_id_input.clear()
            emp_id_input.send_keys(employee_id)
        self.click(self.SAVE_BUTTON)
        # 等待保存成功提示
        self.wait_for_visible(self.SUCCESS_TOAST, timeout=10)
        return True

    @allure.step("搜索员工：{employee_name}")
    def search_employee_by_name(self, employee_name):
        search_box = self.wait_for_visible(self.SEARCH_NAME_INPUT)
        search_box.clear()
        search_box.send_keys(employee_name)
        self.click(self.SEARCH_BUTTON)
        try:
            result = self.wait_for_visible(self.SEARCH_RESULT_NAME, timeout=5)
            return result.text == employee_name
        except:
            return False