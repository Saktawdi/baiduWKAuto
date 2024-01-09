import random
import string
import fake_useragent
import requests
import json

# 实例化 user-agent 对象
ua = fake_useragent.UserAgent()

cookies = ""

identifier = ""

def getTaskList(cid,pageNum):
    headers = {
        'User-Agent': ua.chrome,
        'cookie': cookies,
    }
    params = (
        ('cid', str(cid)),
        ('pn', pageNum),
        ('rn', '20'),
        ('word', ''),
        ('tab', '1'),
    )
    response = requests.get('https://cuttlefish.baidu.com/user/interface/getquerypacklist', headers=headers,
                            params=params)
    return response.text

def getTaskRand():
    headers = {
        'User-Agent': ua.chrome,
        'cookie': cookies,
    }
    response = requests.get('https://cuttlefish.baidu.com/user/interface/gettargetranking', headers=headers)
    return response.text

def getUserInfo():
    headers = {
        'User-Agent': ua.chrome,
        'cookie': cookies,
    }
    params = (
        ('_wkts_', '1679410018416'),
    )
    response = requests.get('https://cuttlefish.baidu.com/ndecommtob/fetchmain', headers=headers, params=params)
    return response.text


# 3
def addUploadFile(md5sum,taskName,token,taskId,docId):
    headers = {
        'User-Agent': ua.chrome,
        'cookie': cookies,
        'Content-Type': 'application/json',
    }
    data = json.dumps({
	"need_process_doc_info_list": {
		docId: {
			"title": taskName,
			"summary": "",
			"tag_str": "",
			"flag": 28,
			"cid1": 0,
			"cid2": 0,
			"cid3": 0,
			"cid4": 0,
			"file_md5sum": md5sum,
			"fold_id": "1661665301",
			"adoptStatus": 0,
			"downloadable": 1,
			"target_product_source": 1
		}
	},
	"token": token,
	"target_product_source": 1,
	"query_id": taskId
})
    response = requests.post('https://cuttlefish.baidu.com/ndecommtob/api/doc/upload/addpublicdoc', headers=headers,
                             data=data)
    return response

# 1
def getPreviewfile(filename,token,fileSize):
    headers = {
        'User-Agent': ua.chrome,
        'cookie': cookies
    }

    data = {
        'filename':filename,
        'identifier': identifier,
        'totalSize': fileSize,
        'file_ext': 'docx',
        'token': token,
        'isMajorTask': '1'
    }

    response = requests.post('https://cuttlefish.baidu.com/doc/newupload/previewfile', headers=headers, data=data)
    return response

# 2
def getCompletefile(filename,identifier,fileTotal,token):
    headers = {
        'User-Agent': ua.chrome,
        'cookie': cookies
    }
    data = {
        'filename': filename,
        'identifier': identifier,
        'totalSize':fileTotal,
        'file_ext': 'docx',
        'token': token
    }

    response = requests.post('https://cuttlefish.baidu.com/doc/newupload/completefile', headers=headers, data=data)


def generate_identifier(length=32):
    # 生成包含大小写字母和数字的字符集
    chars = string.ascii_letters + string.digits
    # 从字符集中随机选择32个字符，拼接成一个字符串
    identifier = ''.join(random.choice(chars) for _ in range(length))
    return identifier

