import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import allure


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="function")
def driver(request):
    headless = request.config.getoption("--headless") or os.getenv("HEADLESS", "").lower() == "true"
    chrome_options = Options()

    # 关键参数（解决 renderer 通信问题）
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")

    # 抑制日志
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 优先使用本地驱动（如果你已手动下载）
    local_driver_path = os.path.join(os.path.dirname(__file__), "drivers", "chromedriver.exe")
    if os.path.exists(local_driver_path):
        service = Service(executable_path=local_driver_path)
        print(f"使用本地 ChromeDriver: {local_driver_path}")
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        os.environ['WDM_URL'] = 'https://registry.npmmirror.com/-/binary/chromedriver'
        service = Service(ChromeDriverManager().install())
        print("使用 webdriver-manager 下载的 ChromeDriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # 不要设置 set_page_load_timeout，让它使用默认的超时（通常足够长）
    # driver.set_page_load_timeout(30)  # 注释掉
    driver.implicitly_wait(10)

    yield driver

    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)