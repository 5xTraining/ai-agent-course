from db.messages import init_message, get_messages, add_message
from tools import get_weather, get_nearby_youbike, get_current_time
from lib.openai import client
from utils.spinner import spinner
from utils.func_tool import function_to_json
from prompt_toolkit import prompt
import json

MODEL_NAME = "gpt-4.1-nano"

AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_nearby_youbike": get_nearby_youbike,
    "get_current_time": get_current_time,
}

init_message(
    """
    你是位厲害的助理，回答問題的時候一律使用**台灣繁體中文**
    不需要幫我進行翻譯，如果回答有中英文混雜，在中文字與英文或數字之間多加空白字元
    """
)

TOOLS = [function_to_json(fn) for fn in AVAILABLE_TOOLS.values()]

print("哈囉，請問有什麼事嗎？")

try:
    while True:
        user_input = prompt("→ ").strip()

        if user_input.lower() == "exit":
            print("再會~")
            break

        if user_input == "":
            continue

        add_message(user_input)

        spinner.start()
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=get_messages(),
            tools=TOOLS,
            tool_choice="auto",
        )

        completion_message = completion.choices[0].message
        tool_calls = completion_message.tool_calls

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

            # 把函數的回傳值交給 LLM 組織成適合人類看的答案
            spinner.start()
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=get_messages(),
            )
            spinner.stop()
            print(response.choices[0].message.content)
        else:
            add_message(completion_message.content, role="assistant")
            spinner.stop()
            print(completion_message.content)
except (EOFError, KeyboardInterrupt):
    print("再會~")
