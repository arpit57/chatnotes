from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import os
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI()

client = chromadb.PersistentClient(path="data")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
google_ef = chromadb.utils.embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GOOGLE_API_KEY)
collection = client.get_collection(name="notes", embedding_function=google_ef)
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
prompt_template = "This prompt has two parts, A question and a similarity text retrieved from a vector database of personal notes. your goal is to answer the question by taking reference from the retrieved text."
class TextData(BaseModel):
    text: str

@app.post("/add-note/")
async def add_note(text_data: TextData):
    collection.add(
    documents=[text_data.text],
    ids=[datetime.datetime.now().strftime('%d-%m-%Y %I:%M %p')]
)
    return {"message": "note saved to database with current timestamp"}

@app.get("/ask-question/")
async def ask_question(question: str):
    results = collection.query(
    query_texts=[question],
    n_results=1)
    retreived_text = results["documents"][0][0]

    prompt = f"{prompt_template} \n question: {question} \n similarity text: {retreived_text}"
    response = llm.invoke(prompt)
    print(prompt)
    return {"answer": response.content}



