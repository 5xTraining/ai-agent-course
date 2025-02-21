from config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

try:
    while True:
        user_question = input("請輸入你的問題(輸入 exit 可結束對話)：")

        if user_question.lower() == "exit":
            print("Bye!")
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 選擇便宜的模型
            messages=[
                {
                    "role": "developer",
                    "content": "你是一位專門講關於貓的笑話大師，回答問題時請一律使用**繁體中文**",
                },
                {
                    "role": "user",
                    "content": user_question,
                },
            ],
        )

        print(response.choices[0].message.content)
except EOFError:
    print("Bye!")
