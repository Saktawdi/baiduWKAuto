import requests
import urllib3

def send_post_request(question, conversation_id):
    headers = {
        'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    }

    params = (
        ('question', question),
        ('conversationId', conversation_id),
    )

    response = requests.get('https://service-8lin0ax8-1254139891.sg.apigw.tencentcs.com/test/', headers=headers,
                            params=params)
    return response.text
