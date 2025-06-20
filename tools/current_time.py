from datetime import datetime


def get_current_time():
    """
    取得現在時間
    """
    return datetime.now().isoformat()
