from lib.openai import client

response1 = client.responses.create(
    model="gpt-4.1-nano",
    instructions="你是一隻貓",
    input="講一個跟貓有關的笑話",
)

print(response1.output_text)

response2 = client.responses.create(
    model="gpt-4.1-nano",
    previous_response_id=response1.id,
    input="跟我說一下為什麼你覺得這個好笑？",
)

print(response2.output_text)
