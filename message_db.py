from tinydb import TinyDB
from datetime import datetime
from time import time

db = TinyDB(f"history/message-{int(time())}.json")


def add_message(content=None, role="user"):
    if content is not None:
        return db.insert(
            {
                "role": role,
                "content": content,
                "created_at": datetime.now().isoformat(),
            }
        )


def get_messages():
    """
    回傳格式：
    [
      {"role": "developer", "content": "...."},
      {"role": "user", "content": "...."},
    ]
    """
    return [
        {
            "role": item["role"],
            "content": item["content"],
        }
        for item in db
    ]


def init_message(content=None):
    """
    初始化資料庫
    """
    db.truncate()

    if content is not None:
        add_message(role="developer", content=content)
