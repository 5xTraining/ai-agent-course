from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import QDRANT_API_KEY, QDRANT_URL
from utils.spinner import spinner
from lib.openai import get_embedding

# 設定每次批量寫入的數量
BATCH_SIZE = 50


class QdrantDB:
    def __init__(self, client=None, collection_name=None):
        """
        初始化 Qdrant 客戶端，若未提供則使用預設設定
        """
        self.client = client or QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        self.batch = []  # 暫存
        self.collection_name = collection_name

    def collection_exist(self, name):
        """
        檢查特定名稱的集合是否已存在
        """
        collection_names = [c.name for c in self.client.get_collections().collections]
        return name in collection_names

    def create_collection(self, name):
        """
        建立新的向量集合，若已存在則跳過
        """
        self.collection_name = name
        if not self.collection_exist(name):
            spinner.start("建立向量資料庫...")
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=1536,  # OpenAI embedding 維度
                    distance=Distance.COSINE,  # 使用餘弦相似度計算向量距離
                ),
            )
            spinner.succeed(f"資料庫 {name} 建立成功!")

    def flush(self):
        """
        將暫存的向量批次寫入資料庫
        """
        if self.batch:
            self.client.upsert(
                collection_name=self.collection_name,
                points=self.batch,
            )
            self.batch = []  # 清空暫存

    def id_exist(self, id):
        """
        檢查特定 ID 的向量是否已存在於資料庫
        """
        existing_point = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[id],
        )

        return len(existing_point) > 0

    def upsert(self, id, text=None, metadata=None):
        """
        將文字轉換為向量並存入批次，當達到批次大小時自動寫入
        """
        if text is not None and not self.id_exist(id):
            self.batch.append(
                {
                    "id": id,
                    "vector": get_embedding(text=text),  # 將文字轉換為向量
                    "payload": metadata or {},  # 儲存額外資料
                }
            )

            # 每 N 筆寫入資料庫
            if len(self.batch) >= BATCH_SIZE:
                self.flush()
