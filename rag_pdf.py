from utils.text import recursive_text_split
from qdrant_db import QdrantDB
from utils.spinner import spinner
import pymupdf
import uuid

if __name__ == "__main__":
    COLLECTION_NAME = "pythonbook"
    vector_db = QdrantDB()
    vector_db.create_collection(COLLECTION_NAME)

    doc = pymupdf.open("data/chapter.pdf")
    for page in doc:
        chunks = recursive_text_split(page.get_text(), chunk_size=1000, overlap=50)

        for text in chunks:
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
            metadata = {
                "page": page.number + 1,
                "text": text,
            }

            spinner.start(f"分析文字：{page.number + 1}/{doc.page_count}")
            vector_db.upsert(
                id=id,
                text=text,
                metadata=metadata,
            )
            spinner.stop()

    vector_db.flush()
    spinner.succeed("資料寫入完成!")
