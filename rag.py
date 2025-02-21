from utils.spinner import spinner
from qdrant_db import QdrantDB
import csv

if __name__ == "__main__":
    COLLECTION_NAME = "netflix"
    vector_db = QdrantDB()
    vector_db.create_collection(COLLECTION_NAME)

    with open("./data/netflix_titles.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            metadata = {
                "type": row["type"],
                "title": row["title"],
                "director": row["director"],
                "cast": row["cast"],
                "release_year": row["release_year"],
                "rating": row["rating"],
                "duration": row["duration"],
                "description": row["description"],
            }

            # 自然語言
            text_input = f"{row['title']} is a {row['type']} directed by {row['director']}, starring {row['cast']}. It was released in {row['release_year']} with a rating of {row['rating']}. The runtime is {row['duration']}. Here's a brief description: {row['description']}."

            id = int(row["show_id"].replace("s", ""))
            spinner.start(f"分析資料：{id} - {row["title"]}")
            vector_db.upsert(
                id=id,
                text=text_input,
                metadata=metadata,
            )
            spinner.stop()

        vector_db.flush()
        spinner.succeed("資料寫入完成!")
