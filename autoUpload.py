import json
import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import win32gui
import win32con
import time

from selenium.webdriver.support.wait import WebDriverWait


def startUpload(titleName, filePath, listName, page):
    page_int = int(page)
    page_int += 1
    page = str(page_int)

    # 创建设置项
    options = webdriver.EdgeOptions()
    # 指定为无界面模式
    # options.add_argument('--headless')
    # 实例化Edge浏览器对象，并将options传入该实例对象
    driver = webdriver.Edge(options=options)

    # 打开目标网页
    driver.get("https://cuttlefish.baidu.com/ndecommtob/browse/index?_wkts_=1690096933618#/taskCenter/majorTask")
    # 首先清除由于浏览器打开已有的cookies
    driver.delete_all_cookies()
    with open('cookies0.json', 'r') as f:
        # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        cookies_list = json.load(f)
        # 方法1 将expiry类型变为int
        for cookie in cookies_list:
            # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
    # 重新进入
    driver.get("https://cuttlefish.baidu.com/ndecommtob/browse/index?_wkts_=1690096933618#/taskCenter/majorTask")
    driver.maximize_window()
    # 等待5秒
    driver.implicitly_wait(5)
    time.sleep(5)
    # 找到 "我知道啦" 这个按钮
    # button = driver.find_element(By.XPATH, "//span[contains(text(), '我知道啦')]/parent::button")
    # button.click()
    # 定位 "实用模板" 元素
    elementText99 = "//div[@class='privilege-item-container action' and contains(text(),'推荐')]"
    if listName == "推荐":
        elementText = "//div[@class='privilege-item-container action' and contains(text(),'"+listName+"')]"
    else:
        elementText = "//div[@class='privilege-item-container' and contains(text(),'"+listName+"')]"
    utility_template_element = driver.find_element(By.XPATH,elementText)
    utility_template_element99 = driver.find_element(By.XPATH,elementText99)
    # 使用ActionChains模拟鼠标点击
    actions = ActionChains(driver)
    # 取消弹窗
    actions.click(utility_template_element99).perform()

    actions.click(utility_template_element).perform()


    print("访问："+listName)
    time.sleep(5)
    # 找到输入框元素
    input_box = driver.find_element(By.CSS_SELECTOR, ".el-pagination__editor input.el-input__inner")
    # 先清空1
    input_box.clear();
    # 在输入框里输入数字
    input_box.send_keys(page)
    # 模拟回车键
    input_box.send_keys(Keys.ENTER)

    print("访问页数：" + page)

    time.sleep(3)
    # 定义指定的doc-title
    target_doc_title = titleName
    # 找到所有类名为"content"的容器
    content_containers = driver.find_elements(By.CLASS_NAME, "content")

    clikcedFlag = False
    # 循环遍历2个容器
    for container in content_containers:
        row_contains = container.find_elements(By.CLASS_NAME, "doc-row")
        if clikcedFlag: break
        for row_contain in row_contains:
            title_element = row_contain.find_element(By.CLASS_NAME, "doc-title")
            # 在当前容器内查找与指定的doc-title相匹配的元素
            if target_doc_title.strip() == title_element.text.strip():
                # 找到匹配的元素，然后查找同一个容器下的上传按钮
                print(title_element.text + "=相等=" + target_doc_title)
                upload_button = row_contain.find_element(By.CLASS_NAME, "upload-btn")
                upload_button.click()
                clikcedFlag = True
                break  # 已找到匹配的元素并点击上传按钮，跳出内层循环
    print("找到目标：" + target_doc_title)
    time.sleep(3)
    # 一级窗口"#32770","打开"；找到窗口，在根据不同浏览器传入 title
    dialog = win32gui.FindWindow("#32770", "打开")
    # 向下传递
    ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
    comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
    # 编辑按钮
    edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
    # 打开按钮
    button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级
    # 输入文件的绝对路径，点击“打开”按钮
    # filePath = os.path.abspath(r"D:\project\pythonProject\baiduwkAuto\立方根方程.docx");
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)  # 发送文件路径
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮
    time.sleep(12)
    driver.implicitly_wait(10)
    # 找到 "确认提交" 按钮
    submit_button = driver.find_element(By.XPATH, "//button[contains(., '确认提交')]")
    # 模拟点击按钮
    submit_button.click()

    print(titleName + "提交成功")

    time.sleep(3)
    # 找到 "查看已提交文档" 按钮
    view_documents_button = driver.find_element(By.XPATH, "//span[contains(text(), '查看已提交文档')]/parent::button")
    # 模拟点击按钮
    if view_documents_button:
        view_documents_button.click()
    time.sleep(3)
    print(titleName + "完成")
    driver.quit()
    pass

# if __name__ == '__main__':
#     startUpload("test", "test", "test", "test");
