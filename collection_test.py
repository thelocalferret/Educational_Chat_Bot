import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
embedding_model = "text-embedding-3-small"

chroma_client = chromadb.PersistentClient(path="/home/ferret/Documents/BachelorThesisCode/chromadb")

collections = chroma_client.list_collections()
print(collections)


#chroma_client.delete_collection(name="teaching_methods_db")
#chroma_client.delete_collection(name="compsci_col")