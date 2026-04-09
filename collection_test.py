import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
embedding_model = "text-embedding-3-small"
path_to_chroma = Path("chromadb")
chroma_client = chromadb.PersistentClient(path=path_to_chroma)

collections = chroma_client.list_collections()
print(collections)


#chroma_client.delete_collection(name="teaching_methods_db")
#chroma_client.delete_collection(name="compsci_col")