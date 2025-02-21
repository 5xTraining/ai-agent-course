import requests
import math

get_nearby_youbike_tool = {
    "type": "function",
    "function": {
        "name": "get_nearby_youbike",
        "description": "取得指定經緯度座標附近可租借的 Youbike 站點",
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "緯度 Latitude",
                },
                "lon": {
                    "type": "number",
                    "description": "經度 longitude",
                },
                "radius": {
                    "type": "number",
                    "description": "範圍半徑，以公尺為單位",
                    "default": 500,
                    "minimum": 0,
                },
                "available_amount": {
                    "type": "number",
                    "description": "可以租借的 Youbike 數量",
                    "default": 0,
                    "minimum": 0,
                },
                "limit": {
                    "type": "number",
                    "description": "顯示筆數",
                    "default": 3,
                },
            },
            "additionalProperties": False,
            "required": ["lat", "lon"],
        },
    },
}


# 計算兩個經緯度之間的距離（Haversine 公式）
def haversine(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
):
    R = 6371000  # 地球半徑 (公尺)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def get_nearby_youbike(
    lat: float,
    lon: float,
    radius: int = 500,
    available_amount: int = 0,
    limit: int = 3,
):
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    data = response.json()

    nearby_stations = []
    for station in data:
        station_lat = float(station["latitude"])
        station_lon = float(station["longitude"])
        distance = haversine(lat, lon, station_lat, station_lon)

        if distance <= radius and station["available_rent_bikes"] > available_amount:
            nearby_stations.append(
                {
                    "station_name": station["sna"].replace("YouBike2.0_", ""),
                    "available_bikes": station["available_rent_bikes"],
                    "distance": int(distance),
                    "address": station["ar"],
                }
            )

    return sorted(nearby_stations, key=lambda x: x["distance"])[:limit]  # 依距離排序
