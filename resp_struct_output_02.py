# 檔案：resp_struct_output_02.py

from lib.openai import client
from pydantic import BaseModel
from typing import List


class Restaurant(BaseModel):
    name: str
    address: str
    rating: float


class RestaurantList(BaseModel):
    results: List[Restaurant]


response = client.responses.parse(
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
    text_format=RestaurantList,
)

print(response.output_text)
