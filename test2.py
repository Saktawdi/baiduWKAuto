import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# 创建Chrome浏览器驱动
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Edge()

# 打开目标网页并登录
driver.get("https://account.wps.cn/?qrcode=kdocs&logo=kdocs&accessid=AK20210823OPGONG&from=v1-web-kdocs-login&cb=https%3A%2F%2Faccount.wps.cn%2Fapi%2Fv3%2Fsession%2Fcorrelate%2Fredirect%3Ft%3D1693468398943%26appid%3D375024576%26cb%3Dhttps%253A%252F%252Fwww.kdocs.cn%252FsingleSign4CST%253Ft%253D1693468398943%2526cb%253Dhttps%25253A%25252F%25252Fwww.kdocs.cn%25252Flatest%25253Ffrom%25253Ddocs")
# 在此处执行登录操作和其他必要操作...

# 等待登录或其他操作完成
# ...
driver.implicitly_wait(5)
try:
    WebDriverWait(driver, 60).until(EC.url_changes(driver.current_url))
    driver.implicitly_wait(5)
    cookies = driver.get_cookies()
except TimeoutException:
    print("Timeout: URL didn't change within 60 seconds")
# 保存Cookie到文件（示例为JSON格式保存）
time.sleep(5)
import json
with open('wps_cookies.json', 'w') as f:
    json.dump(cookies, f)

# 关闭浏览器
driver.quit()
