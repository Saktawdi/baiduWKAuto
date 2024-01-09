import json
import os
from selenium import webdriver
from selenium.common import TimeoutException, exceptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait


def startAutoMake(titleName):
    fileName = titleName + ".PPTX"
    # 当前运行目录
    current_directory = os.getcwd() + "\\taskRes\\"
    # 构建文件的绝对路径
    filePath = os.path.abspath(os.path.join(current_directory, fileName))
    # 创建设置项
    options = webdriver.EdgeOptions()
    # 创建新默认路径与下载设置
    prefs = {"download.default_directory": os.path.abspath(current_directory), "download.prompt_for_download": False}
    # 将创建的下载部分的设置添加到option中
    options.add_experimental_option('prefs', prefs)
    # 指定为无界面模式
    # options.add_argument('--headless')
    # 实例化Edge浏览器对象，并将options传入该实例对象
    driver = webdriver.Edge(options=options)
    # 打开目标网页
    driver.get("https://docer.kdocs.cn/new/wpp/972766879-0?from=docs&reqtype=kdocs&startTime=1693468090848")
    # 首先清除由于浏览器打开已有的cookies
    driver.delete_all_cookies()
    with open('wps_cookies.json', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        # 方法1 将expiry类型变为int
        for cookie in cookies_list:
            # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
    # 重新进入
    driver.get("https://docer.kdocs.cn/new/wpp/972766879-0?from=docs&reqtype=kdocs&startTime=1693468090848")
    driver.maximize_window()
    driver.implicitly_wait(5)



    time.sleep(120)
    pass


if __name__ == '__main__':
    startAutoMake("test")
