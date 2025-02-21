from config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding
