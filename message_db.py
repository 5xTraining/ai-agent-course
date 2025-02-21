from tinydb import TinyDB
from datetime import datetime
from time import time
import json

db = TinyDB(f"history/message-{int(time())}.json")


def add_message(content=None, role="user", **options):
    record = {
        "role": role,
        "content": content,
        "created_at": datetime.now().isoformat(),
    }

    if "tool_calls" in options:
        record["role"] = "assistant"
        record["content"] = None
        record["tool_calls"] = [
            tool_call.model_dump() for tool_call in options.get("tool_calls")
        ]

    if "tool_call_id" in options:
        record["role"] = "tool"
        record["tool_call_id"] = options.get("tool_call_id")
        if not isinstance(content, str) and content is not None:
            record["content"] = json.dumps(content)

    db.insert(record)
    return record


def get_messages():
    """
    回傳格式：
    [
      {"role": "developer", "content": "訊息內容"},
      {"role": "user", "content": "訊息內容"},
      {"role": "assistant", "content": "訊息內容"},
      {"role": "tool", "content": None, "tool_call_id": "call_9527"},
    ]
    """
    excluded_keys = {"id", "created_at"}

    messages = []
    for item in db.all():
        message = {k: v for k, v in item.items() if k not in excluded_keys}
        messages.append(message)

    return messages


def init_message(content=None):
    """
    初始化資料庫
    """
    db.truncate()

    if content is not None:
        add_message(role="developer", content=content)
