import requests
from config import OPEN_WEATHER_API_KEY

get_weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "取得指定城市的即時天氣資訊，包括溫度、濕度、天氣狀況等資訊",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名稱（英文），如 Taipei 或 Tokey",
                }
            },
            "additionalProperties": False,
            "required": ["city"],
        },
    },
}


def get_weather(city: str):
    params = {
        "q": city.lower(),
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric",  # 攝氏
        "lang": "zh_tw",  # 設定語言為繁體中文
    }

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return {
            "city": city,
            "temperature": temperature,
            "description": description,
            "humidity": humidity,
            "wind_speed": wind_speed,
        }
    else:
        return "無法取得天氣資料，請檢查城市名稱或 API 金鑰"
