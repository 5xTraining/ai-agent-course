from config import OPENAI_API_KEY
from openai import OpenAI
from message_db import init_message, add_message, get_messages

client = OpenAI(api_key=OPENAI_API_KEY)

init_message("你是一位專門講關於貓的笑話大師，回答問題時請一律使用**繁體中文**")

try:
    while True:
        user_question = input("請輸入你的問題(輸入 exit 可結束對話)：")

        if user_question.lower() == "exit":
            print("Bye!")
            break

        add_message(user_question.strip())  # 把 user prompt 存起來

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 選擇便宜的模型
            messages=get_messages(),
        )

        content = response.choices[0].message.content
        add_message(content, role="assistant")  # 把 LLM 的回應也存起來

        print(content)
except EOFError:
    print("Bye!")
