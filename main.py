from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import os
import datetime
app = FastAPI()

client = chromadb.PersistentClient(path="data")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
google_ef = chromadb.utils.embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GOOGLE_API_KEY)
collection = client.get_collection(name="notes", embedding_function=google_ef)

class TextData(BaseModel):
    text: str

@app.post("/add-note/")
async def add_note(text_data: TextData):
    collection.add(
    documents=[text_data.text],
    ids=[datetime.datetime.now().strftime('%d-%m-%Y %I:%M %p')]
)
    return {"message": "note saved to database with current timestamp"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
