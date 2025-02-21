from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from config import QDRANT_API_KEY, QDRANT_URL
from utils.spinner import spinner
from llm.openai import get_embedding

BATCH_SIZE = 50


class QdrantDB:
    def __init__(self, client=None, collection_name=None):
        self.client = client or QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        self.batch = []
        self.collection_name = collection_name

    def collection_exist(self, name):
        collection_names = [c.name for c in self.client.get_collections().collections]
        return name in collection_names

    def create_collection(self, name):
        self.collection_name = name
        if not self.collection_exist(name):
            spinner.start("建立向量資料庫...")
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=1536,
                    distance=Distance.COSINE,
                ),
            )
            spinner.succeed(f"資料庫 {name} 建立成功!")

    def flush(self):
        if self.batch:
            self.client.upsert(
                collection_name=self.collection_name,
                points=self.batch,
            )
            self.batch = []

    def id_exist(self, id):
        existing_point = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[id],
        )

        return len(existing_point) > 0

    def upsert(self, id, text=None, metadata=None):
        if text is not None and not self.id_exist(id):
            self.batch.append(
                {
                    "id": id,
                    "vector": get_embedding(text=text),
                    "payload": metadata or {},
                }
            )

            # 每 N 筆寫入資料庫
            if len(self.batch) >= BATCH_SIZE:
                self.flush()
