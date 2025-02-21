from message_db import init_message, get_messages, add_message
from tools.weather import get_weather, get_weather_tool
from llm.openai import client
from utils.spinner import spinner
import json

AVAILABLE_TOOLS = {"get_weather": get_weather}
MODEL_NAME = "gpt-4o-mini"

init_message(
    """
    你是位厲害的助理，回答問題的時候一律使用**繁體中文**
    如果回答有中英文混雜，且在中文字與英文或數字之間多加空白字元
    """
)
add_message("今天台北跟高雄的天氣如何")  # 為求方便，先固定 user 的問題

tools = [get_weather_tool]

spinner.start()
response = client.chat.completions.create(
    model=MODEL_NAME,  # 便宜的模型
    messages=get_messages(),
    tools=tools,
    tool_choice="auto",
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    add_message(tool_calls=tool_calls)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        fn = AVAILABLE_TOOLS.get(function_name)
        if fn is None:  # 如果沒有可執行函數就跳過
            continue

        try:
            args = json.loads(arguments)
        except json.JSONDecodeError:
            args = {}

        result = fn(**args)  # 執行工具！
        add_message(result, tool_call_id=tool_call.id)
    spinner.succeed("取得資料")

    # 交給 LLM 組織答案
    spinner.start()
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=get_messages(),
    )
    spinner.stop()
    print(response.choices[0].message.content)
else:
    print(response_message.content)
