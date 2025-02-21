from qdrant_db import QdrantDB

vector_db = QdrantDB(collection_name="netflix")
search_result = vector_db.search(query="dinosaur")  # 搜尋恐龍電影

print(search_result)
