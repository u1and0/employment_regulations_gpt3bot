"""ChatGPTを使った社則チャットボット"""

import os
# import openai
import requests
import json

# APIキーを環境変数から取得
api_key = os.getenv("CHATGPT_API_KEY")
# openai.api_key = os.getenv("CHATGPT_API_KEY")

# 就業規則のテキストを指定します
policy_text = """
1. 勤務時間は、原則として9:00～17:00とします。
2. 昼食休憩は、原則として12:00～13:00とします。
3. 休憩時間は、勤務時間のうち1日8時間労働につき60分以上を与えます。
4. 出退勤の記録は、原則として電子タイムカードにより行います。
"""

content = f"""弊社の就業規則は下記です。
{policy_text}"""


def ask(question):
    """openaiのモジュール使うとURLが間違っている
    openai.error.InvalidRequestError: Invalid URL (POST /v1/engines/gpt-3.5-turbo/chat/completions)
    のでrequestすることに。
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model":
        "gpt-3.5-turbo",
        "messages": [{
            "role":
            "system",
            "content":
            "就業規則に関連しない質問に対して、「就業規則に関連しない質問には答えられません。」と答えてください。",
        }, {
            "role": "user",
            "content": content,
        }, {
            "role": "user",
            "content": question,
        }],
        "max_tokens":
        1000,
        "temperature":
        0.1  # temparature 0〜1 (default0.7)
        # 0に近いほど関連性の高い単語が選ばれる。
        # 1に近いとより多様な単語が選ばれる。
    }
    return requests.post(url, headers=headers, data=json.dumps(data))
    # response = openai.ChatCompletion.create(engine="gpt-3.5-turbo",
    #                                         messages=[{
    #                                             "role": "user",
    #                                             "content": question
    #                                         }])
    # return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    while True:
        user_input = input("あなた: ")
        if user_input.lower() == "q":
            break
        resp = ask(user_input)
        json_resp = resp.json()
        if resp.status_code == 200:
            answer = json_resp['choices'][0]['message']['content']
            print(f"ChatGPT: {answer}")
        print(json_resp)
