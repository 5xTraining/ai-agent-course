from db.messages import init_message, add_message, get_messages
from lib.openai import client
from tools.weather import get_weather
from utils.spinner import spinner
import json

init_message("你是一位聰明的助理，回答問題的時候請一律使用**台灣繁體中文**")
add_message("今天台北的天氣如何？")  # 為求方便，先固定問題

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "取得指定城市的即時天氣資訊，包括溫度、濕度、天氣狀況等。",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名稱（英文），如 Taipei 或 Tokyo",
                    }
                },
                "additionalProperties": False,
                "required": ["city"],
            },
        },
    }
]

AVAILABLE_TOOLS = {"get_weather": get_weather}

spinner.start()
completion = client.chat.completions.create(
    model="gpt-4.1-nano",  # 選擇便宜的模型
    messages=get_messages(),
    tools=tools,
    tool_choice="auto",
)
spinner.stop()

completion_message = completion.choices[0].message
tool_calls = completion_message.tool_calls

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

        result = fn(**args)
        print(result)
else:
    print(completion_message.content)
