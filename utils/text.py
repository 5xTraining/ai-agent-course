import re


def recursive_text_split(text, chunk_size=500, overlap=50):
    if overlap >= chunk_size:
        raise ValueError("overlap 必須小於 chunk_size")

    sentences = re.split(r"(?<=[。！？\n])", text)  # 用標點符號以及換行來拆分句子

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
