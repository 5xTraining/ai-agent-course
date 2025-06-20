from lib.openai import client

response = client.responses.create(
    model="gpt-4o-mini",
    instructions="你是一個美食專家",
    input="給我 3 家台北車站附近推薦的牛肉麵",
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
    text={
        "format": {
            "type": "json_schema",
            "name": "restaurants",
            "schema": {
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "address": {"type": "string"},
                                "rating": {"type": "number"},
                            },
                            "required": ["name", "address", "rating"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["results"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
)

print(response.output_text)
