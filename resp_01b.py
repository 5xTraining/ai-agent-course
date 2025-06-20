from lib.openai import client

response = client.responses.create(
    model="gpt-4.1-nano",
    instructions="你是一隻貓，請用貓的講話方式",
    input="講一個跟貓有關的笑話",
)

print(response.output_text)
