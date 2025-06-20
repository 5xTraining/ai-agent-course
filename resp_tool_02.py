from lib.openai import client

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="你是一個美食專家",
    input="在台北車站附近最好吃的牛肉麵？",
    tools=[
        {
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "TW",
                "city": "Taipei",
                "region": "Taipei",
            },
        }
    ],
)

print(response.output_text)
