from message_db import init_message, get_messages, add_message
from llm.openai import client

init_message("你是個很聰明的助理，回答問題的時候請一律使用**繁體中文**")
add_message("今天台北的天氣如何")  # 為求方便，先固定 user 的問題

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查詢即時天氣資訊",
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",  # 便宜的模型
    messages=get_messages(),
    tools=tools,
    tool_choice="auto",
)

print(response.choices[0].message)
