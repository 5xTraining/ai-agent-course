from config import OPENAI_API_KEY
from openai import OpenAI
from prompt_toolkit import prompt
from db.messages import init_message, add_message, get_messages

client = OpenAI(api_key=OPENAI_API_KEY)

init_message("你是一位專門講關於貓的笑話大師，回答問題一律使用**台灣繁體中文**")

try:
    while True:
        user_question = prompt("請輸入你的問題：").strip()

        if user_question != "":
            if user_question.lower() == "exit":
                print("再會~")
                break

            add_message(user_question)

            completion = client.chat.completions.create(
                model="gpt-4.1-nano",  # 選擇便宜的模型
                messages=get_messages(),
            )

            content = completion.choices[0].message.content

            add_message(content, role="assistant")  # 把 LLM 的回應也存起來
            print(content)
except EOFError:
    print("再會~")
