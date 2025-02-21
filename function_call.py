from message_db import init_message, get_messages, add_message
from tools import get_weather, get_nearby_youbike, get_current_time, search_netflix
from llm.openai import client
from utils.spinner import spinner
from utils.func_tool import function_to_json
import json

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_nearby_youbike": get_nearby_youbike,
    "get_current_time": get_current_time,
    "search_netflix": search_netflix,
}
MODEL_NAME = "gpt-4o-mini"

init_message(
    """
    - 你是位厲害的助理，回答問題的時候一律使用**台灣繁體中文**
    - 如果是英文的資訊，可以盡量幫我翻譯成**台灣繁體中文**
    - 若回答內容有中英文、數字混合，在中文字與英文及數字之間多加空白
    - 你只能回答使用者提供的工具能處理的請求，如果使用者的請求不在這些工具範圍內，你必須拒絕並回覆
    """
)

TOOLS = [function_to_json(fn) for fn in AVAILABLE_TOOLS.values()]

print("哈囉，請問有什麼事嗎？")

try:
    while True:
        user_input = input("→ ")

        if user_input.lower() == "exit":
            print("Bye!")
            break

        if user_input.strip() == "":
            continue

        add_message(user_input.strip())

        spinner.start()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=get_messages(),
            tools=TOOLS,
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
            add_message(response_message.content, role="assistant")
            spinner.stop()
            print(response_message.content)
except EOFError:
    print("Bye!")
