import ast
import os
import random
import re
import sys
import time
import webbrowser

import WkApi
import json

import autoMakePPT
import chatGPTApi
from autoUpload import startUpload
from login import login, get_user_info, getAppInfo
from multiprocess import *
import requests
from tqdm import tqdm

# 应用版本
global m_version
m_version = "1.3.2"
global orderCid
orderCid = -1
# 第一页开始下标 0 - 19
global startIndex
startIndex = -1
# 开局第n + 1页 0 -9
global startPage
startPage = "1"

listName = ["推荐", "学前教育", "基础教育", "高校与高等教育", "语言/资格考试", "法律", "建筑", "互联网", "行业资料", "政务民生", "商品说明书", "实用模板",
            "生活娱乐"]


# 读取任务队列
def read_array_from_file(fileName):
    content = ""
    try:
        with open(fileName, 'r') as file:
            content = file.read().strip()
    except FileNotFoundError:
        print("任务列表文件不存在")
        content = get_user_input("请输入任务列表:")
        with open('orderList.txt', 'w') as file:
            file.write(content)
    # array_strings = content.split(',')
    if content == "":
        print("没有任务")
        content = get_user_input("请输入任务列表:")
        with open('orderList.txt', 'w') as file:
            file.write(content)
    array_list = ast.literal_eval(content)
    return array_list


# 判断生成ppt失败队列是否为空
def isUploadFailedListEmpty():
    try:
        with open("failedList.txt", 'r') as file:
            content = file.read().strip()
        if content == "[]" or content == "":
            return True
        return False
    except FileNotFoundError:
        return True

# 入口
def getSysParam():
    print("登录百度......")
    if WkApi.cookies != "":
        userRes = json.loads(WkApi.getUserInfo())
        taskRandRes = json.loads(WkApi.getTaskRand())
        if userRes['pageData']['upUserInfo']['status']['code'] == 200001:
            print("cookies过期,请重新登录")
            return
        userUid = userRes['pageData']['upUserInfo']['data']['uid']
        userToken = userRes['pageData']['upUserInfo']['data']['token']
        userName = userRes['pageData']['upUserInfo']['data']['uname']
        if taskRandRes['status']['msg'] != "empty list":
            completeCount = taskRandRes['data']['currentUser']['completeCount']
            rank = taskRandRes['data']['currentUser']['rank']
        print("百度用户登录完成：", userName)
        # 新逻辑 V1.1
        if input("选择启动模块：1.生成ppt 2.自动上传  1 or 2:") == "1":
            array_list = read_array_from_file("orderList.txt")
            if not isUploadFailedListEmpty():
                if input("生成失败列表不为空，是否继续生成ppt? y/n") == "y":
                    array_list = read_array_from_file("failedList.txt")
            if input("选择ppt网站的生成模式，1.AI * AI，2.粘贴MD") == "1":
                autoDealTaskByList(2,array_list)
            else:
                autoDealTaskByList(1,array_list)
        else:
            success_list = read_array_from_file("orderList.txt")
            autoUploadByList(success_list)
        # getTaskList(userName, userUid)
    else:
        print("百度cookies为空,请重新尝试")
    pass


# 生成ppt 加 自动上传
def autoDealTaskByList(choice,array_list):
    failed_list = []
    if array_list:
        for array in array_list:
            orderCid = array[0]
            startPage = array[1]
            startIndex = array[2]
            if orderCid == 99:
                tempCid = 0
            else:
                tempCid = orderCid + 1
            taskRes = json.loads(WkApi.getTaskList(orderCid, startPage))
            if taskRes['status']['code'] == 0:
                taskList = taskRes['data']['queryList']
                if not taskList:
                    print(listName[tempCid] + "下没有任务了！！")
                    continue
                task = taskList[startIndex]
                taskName = task['queryName']
                if task['status'] == 2:
                    print(taskName + "任务被抢先了")
                    continue
                else:
                    print(taskName + "ppt任务开始执行，序列:" + str(array))
                    taskRes = AIRes(taskName)
                    try:
                        if autoMakePPT.startAutoMake(taskName, taskRes, choice) == False:
                            failed_list.append(array)
                    except Exception as e:
                        print("ppt任务执行异常")
                        failed_list.append(array)

    else:
        print("No arrays found in the file.")

    with open('failedList.txt', 'w') as file:
        file.write(str(failed_list))
    autoUploadByList(array_list)
    pass


# 自动上传
def autoUploadByList(success_list):
    uploadFailedList = []
    choice = ".pdf";
    if input("请选择上传文件类型：1.pdf；2.pptx") == "2":
        choice = ".pptx"
    # 当前运行目录
    current_directory = os.getcwd() + "\\taskRes\\"
    # 遍历success_list
    for array in success_list:
        orderCid = array[0]
        startPage = array[1]
        startIndex = array[2]
        # 插入等待
        pasue = random.random() * 1.2
        time.sleep(pasue)
        taskRes = json.loads(WkApi.getTaskList(orderCid, startPage))
        if orderCid == 99:
            tempCid = 0
        else:
            tempCid = orderCid + 1
        if taskRes['status']['code'] == 0:
            taskList = taskRes['data']['queryList']
            task = taskList[startIndex]
            if task['status'] == 2:
                print(task['queryName'] + "任务被抢先了")
                continue
            taskName = task['queryName']
            fileName = taskName + choice
            # 构建文件的绝对路径
            filePath = os.path.abspath(os.path.join(current_directory, fileName))
            if os.path.exists(filePath):
                try:
                    startUpload(taskName, filePath, listName[tempCid], startPage);
                except Exception as e:
                    print(str(array) + "序列上传异常")
                    uploadFailedList.append(array)
            else:
                print(taskName + ":文件不存在,跳过")
                continue
        else:
            print(taskName + "请求失败")
            continue
    with open('uploadFailedList.txt', 'w') as file:
        file.write(str(uploadFailedList))
    print("执行完毕，请到官网自行检查")
    input("按任意键退出")
    sys.exit()


pass


# ai 作答
def AIRes(taskName):
    print("正在等待AI作答......" + taskName)
    for i in range(3):
        print("第" + str(i + 1) + "次尝试...")
        response = None
        response = chatGPTApi.sendMsg("帮我做一份有关《" + taskName + "》的PPT，用markdown代码框进行输出,文案丰富点，最少2500字。")
        if not response:
            continue
        taskRes = response
        taskRes.replace("作为一名AI机器人", "")
        taskRes.replace("AI", "")
        taskRes.replace("机器人", "")
        taskRes.replace("好的,", "")
        taskRes.replace("我重新用普通的语言描述如下:", "")
        taskRes.replace("作为人工智能语言模型，我没有个人观点或情感,", "")
        taskRes.replace("至2500字", "")
        taskRes.replace("2500字", "")
        taskRes.replace("更多", "一些")
        print("AI:" + taskRes)
        return taskRes


# old
def getTaskList(userName, userUid):
    listCid = [99, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    listName = ["推荐", "学前教育", "基础教育", "高校与高等教育", "语言/资格考试", "法律", "建筑", "互联网", "行业资料", "政务民生", "商品说明书", "实用模板", "生活娱乐"]
    canUsedCid = []
    taskRes = []
    for cid in listCid:
        taskRes = json.loads(WkApi.getTaskList(cid, startPage))
        if cid == 99:
            print("获取列表：" + listName[0])
        else:
            print("获取列表:" + listName[cid + 1])
        if taskRes['status']['code'] != 0:
            for i in range(3):
                if taskRes['status']['code'] == 0: break
                taskRes = json.loads(WkApi.getTaskList(cid, startPage))
        if not taskRes['data']['queryList']:
            continue
        else:
            canUsedCid.append(cid)
            if cid == 99:
                nowUsingListName = listName[0]
            else:
                nowUsingListName = listName[cid + 1]
    print("最新可用id:", canUsedCid)
    for nowCid in canUsedCid:
        global orderCid
        if orderCid != -1:
            nowCid = orderCid
            orderCid = -1
        # 插入等待
        pasue = random.random() * 5
        time.sleep(pasue)

        tempCid = nowCid
        if (nowCid == 99):
            tempCid = 0
        else:
            tempCid = nowCid + 1
        if taskRes['status']['code'] != 0:
            print(listName[tempCid] + "任务没了")
            continue;
        taskList = taskRes['data']['queryList']
        if not taskList:
            print(listName[tempCid] + "任务没了")
        else:
            print("任务列表：[" + listName[tempCid] + "]正在攻略......")
            taskFinishNum = taskRes['data']['userFinishTaskNum']
            print("完成任务数:", taskFinishNum)
            taskUpDayNum = taskRes['data']['uploadDayNum']
            print("已上传天数", taskUpDayNum)
            taskNextAward = taskRes['data']['nextLevelAward']
            taskNextNeed = taskRes['data']['nextLevelNeedTask']
            print("距离下个奖金:" + str(taskNextAward) + "\t还需要任务数:+" + str(taskNextNeed))
            taskAllNum = taskRes['data']['total']
            if startPage != "-1":
                dealTask(taskList, userName, listName[tempCid], startPage)
            else:
                # 处理第一页
                dealTask(taskList, userName, listName[tempCid], "1")
    pass


# old
def dealTask(taskList, userName, listName, pageNum):
    print("正在处理...")
    global startIndex
    if startIndex != -1:
        index = startIndex
        startIndex = -1
    else:
        index = 0
    while index < len(taskList):
        task = taskList[index]
        index = index + 1
        if task['status'] == 2:
            continue
        queryId = task['queryId']
        taskName = task['queryName']
        # 规避词汇 敏感词
        sensitive_words = ["谱", "电子课本", "字帖", "照片", "试卷"]
        pattern = "|".join(sensitive_words)
        if re.search(pattern, taskName):
            continue
        else:
            taskRes = AIRes(taskName)
            # 保存doc文档
            # doc = Document()
            # doc.add_heading(taskName, level=1)
            # doc.add_paragraph(taskRes)
            # fileName = "taskRes/" + taskName + ".docx"
            # doc.save(fileName)
            # # 获取当前运行目录
            # current_directory = os.getcwd()
            # # 构建文件的绝对路径
            # filePath = os.path.abspath(os.path.join(current_directory, fileName))
            # 生成ppt
            filePath = autoMakePPT.startAutoMake(taskName, taskRes, userName)
            startUpload(taskName, filePath, listName, pageNum)
            break
            print("正在继续下一个有效任务")
    pass


def save_token_to_file(token):
    try:
        with open('token.txt', 'w') as file:
            file.write(token)
            file.close()
            print("保存token成功")
    except:
        print("保存token失败")
        pass


def get_user_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():  # Check if the input is not empty after removing leading/trailing spaces
            return user_input
        print("输入不能为空，请重新输入。")


# 用户登录
def loadUserInfo():
    username = get_user_input("请输入账户: ")
    password = get_user_input("请输入密码: ")
    token = login(username, password)
    if token['code'] == 0:
        tokenStr = token['token']
        info = get_user_info(tokenStr)
        if info['code'] == 0:
            userDept = info['data']['dept']['deptName']
            if userDept == "脚本用户" or userDept == "超级管理员":
                print("登录成功,是否选择记录用户？")
                if input("请输入y或n: ") == "y":
                    save_token_to_file(tokenStr)
            else:
                print("权限不够，请联系管理员")
                input("按回车键继续...")
                sys.exit()
        else:
            print(info['msg'])
            input("按回车键继续...")
            sys.exit()
    else:
        print(token['msg'])
        input("按回车键继续...")
        sys.exit()


# 版本号比较
def compare_versions(new_version, current_version):
    new_version_parts = list(map(int, new_version.split('.')))
    current_version_parts = list(map(int, current_version.split('.')))

    for i in range(max(len(new_version_parts), len(current_version_parts))):
        new_part = new_version_parts[i] if i < len(new_version_parts) else 0
        current_part = current_version_parts[i] if i < len(current_version_parts) else 0

        if new_part > current_part:
            return 1  # New version is greater
        elif new_part < current_part:
            return -1  # Current version is greater

    return 0  # Versions are equal


# 在线更新
# todo:后台shiro更新
def updateApp(downLoadUrl):
    eg_link = downLoadUrl
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(eg_link, headers=headers, stream=True)
    with tqdm.wrapattr(open(eg_link.split('/')[-1], "wb"), "write",
                       miniters=1, desc=eg_link.split('/')[-1],
                       total=int(response.headers.get('content-length', 0))) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)
    time.sleep(1)
    pass


if __name__ == '__main__':
    os.system("cls")
    print("输入回车键继续...", flush=True)
    print("正在获取最新版本：", flush=True)
    app_id = 2
    appInfo = getAppInfo(app_id)
    version = appInfo['data']['appVersion']
    result = compare_versions(version, m_version)
    if result == 1:
        print("发现新版本！V" + version, flush=True)
        print("更新日志：", flush=True)
        print(appInfo['data']['description'], flush=True)
        input("按回车键更新...")
        updateApp(appInfo['data']['downloadUrl'])
        input("按回车键继续...")
        sys.exit()
    else:
        print("当前版本已经是最新版本")
        input("按回车键继续...")
    try:
        file = open("cookies0.txt", "r")
        content = file.read()
        WkApi.cookies = content
        file.close()
    except FileNotFoundError:
        print("输入cookies:")
        s = input()
        WkApi.cookies = s
        file = open("cookies0.txt", "w").write(WkApi.cookies)
    try:
        fileToken = open("token.txt", "r")
        token = fileToken.read()
        if token:
            info = get_user_info(token)
            if info['code'] == 0:
                userDept = info['data']['dept']['deptName']
                if userDept == "脚本用户" or userDept == "超级管理员":
                    print("登录成功")
                else:
                    print("权限不够，请联系管理员")
                    input("按回车键继续...")
                    sys.exit()
            elif info['msg'] == "token已过期":
                print("登录过期，请重新登录", flush=True)
                loadUserInfo()
            else:
                print(info['msg'])
                sys.exit()
        else:
            loadUserInfo()
        fileToken.close()
    except FileNotFoundError:
        loadUserInfo()
    getSysParam()
    pass
