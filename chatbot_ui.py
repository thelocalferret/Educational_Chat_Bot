from tkinter import *
from tkinter import ttk
from chatbot_proto_0 import retrieve, retrieve_study, sentence_window_retrieval, QueryVariations, QueryVars, ask_with_context
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import chromadb
from pathlib import Path
import os

openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
path_to_chroma = Path("chromadb")
chroma_client = chromadb.PersistentClient(path=path_to_chroma)
embedding_model = "text-embedding-3-small"
collection_1 = chroma_client.get_collection(name="teaching_methods_db")
collection_2 = chroma_client.get_collection(name="compsci_col")

root = Tk()

root.title('Bachelor Thesis')
root.geometry('720x400+150+100')
root.configure(bg='MediumPurple1')
root.resizable(False, False)

chat_history = Text(root, fg='black', border=2, bg='white', height=15, width=86, font=("calibri", 11))
chat_history.place(x=10, y=20)
prompt_var = StringVar()
question = Entry(root, textvariable = prompt_var, width=66, font=("calibri", 11))
question.place(x=10, y=350)

def get_prompt(event):
    prompt = prompt_var.get()
    answer = ask_with_context(prompt)
    chat_history.config(state=NORMAL)
    chat_history.insert(END, f"You: {prompt}\n\n")
    chat_history.insert(END, f"AI: {answer}\n\n")
    chat_history.config(state=DISABLED)
    prompt_var.set("")

send_button = Button(root, text='Send', command= lambda: get_prompt(event='<Key>'))
send_button.place(x=550, y=350)
root.bind('<Return>', get_prompt)

root.mainloop()