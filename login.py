import requests


def login(username, password):
    url = 'http://183.56.226.207:7868/v1/user/pub/login'
    headers = {'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/'}
    data = {'username': username, 'password': password}
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception if the request is not successful (status code >= 400)
        responseData = response.json()
        return responseData
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


def get_user_info(token):
    url = 'http://183.56.226.207:7868/v1/user/pri/getInfo'
    headers = {
        'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
        'token': token
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            return response.json()
        elif response.status_code == 200:
            responseData = response.json()
            return responseData
        else:
            print(f"Unexpected response: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None


def getAppInfo(appId):
    url = 'http://183.56.226.207:7868/v1/app/pub/getInfo'
    headers = {
        'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/'
    }
    data = {
        'appId': appId  # Use the Long object wrapper for the 'appId' parameter
    }
    try:
        response = requests.get(url, headers=headers, params=data)
        response.raise_for_status()  # Raise an exception if the request is not successful (status code >= 400)
        responseData = response.json()
        # Process the response data here
        return responseData
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None