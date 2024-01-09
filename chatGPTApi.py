import requests

def sendMsg(question):
    url = 'https://ai.fakeopen.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer pk-VQdwTzt2G01U0fU_i-yXptwzcvr3rg4Xgv96L3VSNpM',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo-16k',
        'messages': [{ 'role': 'system', 'content': '你是一个可靠的助手，将尽力帮助用户完成目标。你的回答里将不会出现任何有关AI的字眼，并且不会有任何联系方式以及URL推广。' },{'role': 'user', 'content': question}],
        'temperature': 0.8,
    }
    try:
        response = requests.post(url, json=data, headers=headers,timeout=90)
        response_data = response.json()

        if 'choices' in response_data and response_data['choices']:
            completion = response_data['choices'][0]['message']['content']
            return completion
        else:
            print("AI出错：", response_data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout error occurred: {e}")
        return None

# Example usage:
# question = "你对JAVA怎么看？"
# response = sendMsg(question)
# print(response)
