from openai import OpenAI
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
path_to_chroma = Path("chromadb")
chroma = chromadb.PersistentClient(path=path_to_chroma)
embedding_model = "text-embedding-3-small"

def chunk_text(text, size=1000, overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            bp = text.rfind("\n\n", start, end)
            if bp == -1:
                bp == text.rfind(". ", start, end)
            if bp > start:
                end = bp + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end < len(text) else end
    return chunks

def embed_and_store(chunks, db_path, collection_name, description):
    collection = chroma.get_or_create_collection(
        name=collection_name,
        metadata={"description": description}
    )
    embeddings = []
    for i in range(0, len(chunks), 100):
        batch = chunks[i : i + 100]
        res = client.embeddings.create(model=embedding_model, input=batch)
        embeddings.extend([x.embedding for x in res.data])

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"chunk_index": i} for i in range(len(chunks))],
    )
    return collection

file_path = Path("teaching_methods.txt")
text = file_path.read_text(encoding="utf-8")
chunks = chunk_text(text)

file_path_text_2 = Path("think_python.txt")
text_2 = file_path_text_2.read_text(encoding="utf-8")
chunks_2 = chunk_text(text_2)

collection = embed_and_store(chunks, path_to_chroma, "teaching_methods_db", "Database of teaching methods")
collection_2 = embed_and_store(chunks_2, path_to_chroma, "compsci_col", "Database of study materials on computer science")