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


def startAutoMake(titleName, content, choice = 2):
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
    options.add_argument('--headless')

    # 实例化Edge浏览器对象，并将options传入该实例对象
    driver = webdriver.Edge(options=options)

    # 打开目标网页
    driver.get("https://www.mindshow.fun/#/login")
    driver.maximize_window()
    driver.implicitly_wait(5)
    # 登录
    # Locate the email/phone number input field and the "立即登录" button
    email_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入您的邮箱/手机号']")
    login_button = driver.find_element(By.XPATH, "//div[@class='login_btn'][contains(text(), '立即登录')]")
    # Enter the email/phone number into the input field
    email_input.send_keys("17896630848")
    # Click the "立即登录" button
    login_button.click()
    driver.implicitly_wait(5)
    pwd_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入密码']")
    pwd_input.send_keys("www.scf520")
    yes_button = driver.find_element(By.XPATH, "//div[@class='login_btn'][contains(text(), '登录')]")
    yes_button.click()
    driver.implicitly_wait(5)

    time.sleep(1)
    # 关闭试用会员弹窗
    # closeAD_button = driver.find_element(By.XPATH,
    #                                      "//button[@class='absolute block top-28px right-60px h-24px w-24px']")
    # if closeAD_button:
    #     closeAD_button.click()
    # time.sleep(1)

    # 导入粘贴
    if choice == 1:
        import_elements = driver.find_element(By.ID, "import")
        action = ActionChains(driver)
        action.click(import_elements).perform()

        md_input = driver.find_element(By.XPATH, "//textarea[@placeholder='请输入或粘贴需要导入的内容']")
        md_input.send_keys(content)

        make_button = driver.find_element(By.XPATH, "//button[@class='clickbutton' and contains(text(), '导入创建')]")
        make_button.click()
    elif choice == 2:
        # 更多选项，配置
        more_elements = driver.find_element(By.XPATH, "//div[@class='chatgptclickmore']")
        action = ActionChains(driver)
        action.click(more_elements).perform()

        aidrawer_elements = driver.find_element(By.CLASS_NAME, "aidrawer_left")
        taskInput = aidrawer_elements.find_element(By.CLASS_NAME, 'ant-input')
        taskInput.send_keys(titleName)
        text_area = aidrawer_elements.find_element(By.CSS_SELECTOR, 'textarea.ant-input')
        text_area.send_keys(content)
        make_button = aidrawer_elements.find_element(By.XPATH,
                                                     "//button[@class='ant-btn ant-btn-primary' and span='AI生成内容']")
        make_button.click()
        print("等待PPT生成内容完毕......")

        # 等10秒
        time.sleep(10)

        make_button = driver.find_element(By.XPATH, "//button[@class='ant-btn ant-btn-primary' and span='生成PPT']")
        flag = False
        while flag == False:
            try:
                if make_button.is_displayed():
                    flag = True
                    make_button.click()
            except:
                pass

    try:
        WebDriverWait(driver, 120).until(EC.url_changes(driver.current_url))
        print("生成完毕：正在更改小部分信息")
    except TimeoutException:
        print("Timeout: URL didn't change within 120 seconds")
    driver.implicitly_wait(15)
    time.sleep(5)
    # # 刷新
    # driver.refresh()
    driver.implicitly_wait(20)
    # 演讲标题
    presentation_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入演讲标题']")
    presentation_input.clear()
    presentation_input.send_keys(titleName)
    # 演讲者
    speaker_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入演讲者']")
    speaker_input.clear()
    speaker_input.send_keys('  ')
    # 副标题
    subTitle_input = driver.find_element(By.XPATH, "//input[@placeholder='请输入副标题']")
    subTitle_input.clear()
    subTitle_input.send_keys('  ')

    # 免费标签
    free = driver.find_element(By.XPATH, "//span[@class='filter_item' and contains(text(), '免费')]")
    action = ActionChains(driver)
    action.click(free).perform()
    time.sleep(1)

    random = driver.find_element(By.XPATH, "//div[@class='m2p_r_theme_item']")
    action = ActionChains(driver)
    action.click(random).perform()

    # 使用 JavaScript 代码触发弹窗提示
    # message = "你有10秒的空窗期j进行检查，之后程序会点击下载pptx"
    # script = f"alert('{message}');"
    # driver.execute_script(script)
    time.sleep(5)

    # subTitle_input.send_keys(userName + "（百度ID）的图文系列")
    # todo:随机主题
    # print("随机主题")
    # # 使用XPath定位元素
    # img_element = driver.find_element(By.XPATH, "//img[@alt='推荐主题']")
    # # 使用鼠标操作模拟点击
    # actions = ActionChains(driver)
    # actions.move_to_element(img_element).click().perform()
    # # 主题父容器
    # load_divs = driver.find_elements(By.CLASS_NAME,"ant-spin-nested-loading")
    # load_div = load_divs[0]
    # # 等待子容器消失
    # timeout = 12  # s
    # interval = 1  # s
    # for _ in range(timeout):
    #     time.sleep(interval)
    #     try:
    #         load_div.find_element(By.CLASS_NAME, "ant-spin-container ant-spin-blur")
    #         continue
    #     except exceptions.NoSuchElementException:
    #         print("加载完毕")
    #         break
    # # 再次点击
    # print("再次随机")
    # actions.move_to_element(img_element).click().perform()
    # # 等待子容器消失
    # for _ in range(timeout):
    #     time.sleep(interval)
    #     try:
    #         load_div.find_element(By.CLASS_NAME, "ant-spin-container ant-spin-blur")
    #         continue
    #     except exceptions.NoSuchElementException:
    #         print("加载完毕")
    #         break

    # 下载
    download_button = driver.find_element(By.ID, "m2p_r_ppt_share_btn")
    download_button.click()
    # PPTX格式
    PPTX_format_element = driver.find_element(By.XPATH, "//span[@class='dropdown_style' and contains(text(), 'PPTX格式')]")
    # 模拟"PPTX格式"
    actions = ActionChains(driver)
    actions.move_to_element(PPTX_format_element)
    actions.click(PPTX_format_element)
    actions.perform()
    print("等待PPTX文件下载完成......")
    # 检测是否下载完成
    timeout = 60  # s
    interval = 1  # s
    download_completed = False
    for _ in range(timeout):
        if os.path.exists(filePath):
            if os.path.getsize(filePath) <= 1024:
                download_completed = False
            else:
                download_completed = True
            break
        time.sleep(interval)
    driver.quit()
    if download_completed:
        print(titleName + "PPTX文件下载完成！")
        return True
    else:
        print(titleName + "PPTX文件下载超时或异常！")
        return False

# if __name__ == '__main__':
#     ppt_content = """
#     **《初见花里藏头诗》PPT**
#     """
#     startAutoMake("初见花里藏头诗", ppt_content,2)
