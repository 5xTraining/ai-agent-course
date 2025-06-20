from config import OPENAI_API_KEY
from openai import OpenAI
from prompt_toolkit import prompt

client = OpenAI(api_key=OPENAI_API_KEY)

try:
    while True:
        user_question = prompt("請輸入你的問題：").strip()

        if user_question != "":
            if user_question.lower() == "exit":
                print("再會~")
                break

            completion = client.chat.completions.create(
                model="gpt-4.1-nano",  # 選擇便宜的模型
                messages=[
                    {
                        "role": "developer",
                        "content": "你是一位專門講關於貓的笑話大師，回答問題一律使用**台灣繁體中文**",
                    },
                    {
                        "role": "user",
                        "content": user_question,
                    },
                ],
            )

            print(completion.choices[0].message.content)
except EOFError:
    print("再會~")
