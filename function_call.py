from db.messages import init_message, add_message, get_messages
from lib.openai import client

init_message("你是一位聰明的助理，回答問題的時候請一律使用**台灣繁體中文**")
add_message("今天台北的天氣如何")  # 為求方便，先固定問題

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查詢即時天氣資訊",
        },
    }
]

completion = client.chat.completions.create(
    model="gpt-4.1-nano",  # 選擇便宜的模型
    messages=get_messages(),
    tools=tools,
    tool_choice="auto",
)

print(completion.choices[0].message)
