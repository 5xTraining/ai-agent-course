# 檔案：resp_01a.py

from lib.openai import client

response = client.responses.create(
    model="gpt-4.1-nano",
    input=[
        {"role": "developer", "content": "你是一隻貓，請用貓的講話方式"},
        {"role": "user", "content": "講一個跟貓有關的笑話"},
    ],
)

print(response.output_text)
