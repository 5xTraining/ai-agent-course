from lib.openai import client
from tools import get_current_time, get_weather, get_nearby_youbike
from utils.func_tool import function_to_json_v2
from prompt_toolkit import prompt

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_nearby_youbike": get_nearby_youbike,
    "get_current_time": get_current_time,
}

TOOLS = [function_to_json_v2(fn) for fn in AVAILABLE_TOOLS.values()]

print("哈囉，請問有什麼事嗎？")

try:
    while True:
        user_input = prompt("→ ").strip()

        if user_input != "":
            response = client.responses.create(
                model="gpt-4.1-nano",
                instructions="""
                - 你是位厲害的助理，回答問題的時候一律使用**台灣繁體中文**
                - 如果是英文的資訊，盡量幫我翻譯成**台灣繁體中文**
                - 若回答內容有中英文、數字混合，在中文字與英文及數字之間多加空白
                - 你只能回答使用者提供的工具能處理的請求，如果使用者的請求不在這些工具範圍內，你必須拒絕並回覆
                """,
                input=user_input,
                tools=TOOLS,
            )

            print(response.output)
except (EOFError, KeyboardInterrupt):
    print("再會~")
