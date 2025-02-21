from message_db import init_message, get_messages, add_message
from tools.weather import get_weather
from llm.openai import client
from utils.spinner import spinner
import json

init_message("你是個很聰明的助理，回答問題的時候請一律使用**繁體中文**")
add_message("今天台北的天氣如何")  # 為求方便，先固定 user 的問題

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "取得指定城市的即時天氣資訊，包括溫度、濕度、天氣狀況等資訊",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名稱（英文），如 Taipei 或 Tokey",
                    }
                },
                "additionalProperties": False,
                "required": ["city"],
            },
        },
    }
]

spinner.start()
response = client.chat.completions.create(
    model="gpt-4o-mini",  # 便宜的模型
    messages=get_messages(),
    tools=tools,
    tool_choice="auto",
)
spinner.stop()

response_message = response.choices[0].message
tool_calls = response_message.tool_calls

AVAILABLE_TOOLS = {"get_weather": get_weather}

if tool_calls:
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        fn = AVAILABLE_TOOLS.get(function_name)
        if fn is None:
            continue

        try:
            args = json.loads(arguments)
        except json.JSONDecodeError:
            args = {}

        result = fn(**args)  # 執行工具！
        print(result)
else:
    print(response_message.content)
