from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
chroma_client = chromadb.PersistentClient(path="/home/ferret/Documents/BachelorThesisCode/chromadb")
embedding_model = "text-embedding-3-small"
collection_1 = chroma_client.get_collection(name="teaching_methods_db")
collection_2 = chroma_client.get_collection(name="compsci_col")

def retrieve(question, top_k=3):
    q_emb = client.embeddings.create(
        model=embedding_model,
        input=question,
    ).data[0].embedding

    res = collection_1.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents"],
    )
    return res["documents"][0]

def retrieve_study(question, top_k=3):
    q_emb = client.embeddings.create(
        model=embedding_model,
        input=question,
    ).data[0].embedding

    res = collection_2.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents"],
    )
    return res["documents"][0]

class QueryVariations(BaseModel):
    queries: list[str]

def QueryVars(question):
    query_variations_prompt = f"""You are an AI language model assistant. Your task is
    to create three alternative versions of the provided user query to
    enhance the retrieval of relevant documents from a vector database.
    By offering diverse variations of the query, your goal is to help
    mitigate the limitations of distance-based similarity search. Provide
    these alternative queries, each on a new line.

    Original query: {question}"""

    completion = client.beta.chat.completions.parse(
        model="gpt-5-mini",
        messages=[
            {
                "role": "user",
                "content": query_variations_prompt,
            },
        ],
        response_format=QueryVariations,
    )
    queries = completion.choices[0].message.parsed.queries
    return queries

def sentence_window_retrieval(question, top_k=3):
    q_emb = client.embeddings.create(
        model=embedding_model,
        input=question,
    ).data[0].embedding

    temp = collection_2.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas"]
    )
    
    id = temp["metadatas"][0][0]['chunk_index']

    if id != 0:
        res = collection_2.get(
            ids=[f"chunk_{id-1}", f"chunk_{id}", f"chunk_{id+1}"],
        )
    return res["documents"]

def ask_with_context(question):
    queries = QueryVars(question)
    add_context = ""
    for i in queries:
        add_context += "\n\n---\n\n".join(retrieve_study(i))
    
    teaching_context = "\n\n---\n\n".join(retrieve(question))
    material_context = "\n\n---\n\n".join(retrieve_study(question))
    material_context_2 = "\n\n---\n\n".join(sentence_window_retrieval(question))
    messages= [
        {
            "role": "system",
            "content": "You are an educational chatbot, your task is to guide the user to the answer without directly stating it. You are a Socratic teacher. Use the Teaching Context as your guidelines."
        },
        {
            "role": "user",
            "content": f"Teaching Context:\n{teaching_context}\n\nMaterial Context:\n{material_context}\n{add_context}\n{material_context_2}\n\nQuestion:\n{question}"
        },
    ]

    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=messages
    )

    return response.choices[0].message.content

print("Type Exit to finish process.")
while True:
    question = input("Enter your prompt: ")
    if question == "Exit":
        break
    answer = ask_with_context(question)
    print(answer)
