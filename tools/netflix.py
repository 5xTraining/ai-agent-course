from qdrant_db import QdrantDB


def search_netflix(query: str):
    """
    查詢 Netflix 影片資料庫
    參數：
      query: 電影片名、導演、種類、分級或是影片描述，請使用英文查詢
    """

    db = QdrantDB(collection_name="netflix")
    return db.search(query=query)
