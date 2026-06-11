from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("开始下载/获取 ChromeDriver...")
service = Service(ChromeDriverManager().install())
print("ChromeDriver 路径:", service.path)

options = webdriver.ChromeOptions()
options.add_argument("--remote-allow-origins=*")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

print("启动 Chrome 浏览器...")
driver = webdriver.Chrome(service=service, options=options)
print("Chrome 已启动，尝试访问百度...")
driver.get("https://www.baidu.com")
print("页面标题:", driver.title)
time.sleep(2)
driver.quit()
print("测试成功！")