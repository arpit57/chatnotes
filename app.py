from fastapi import FastAPI
import os
from chromadb.api import API
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SimpleEmbeddingFunction

app = FastAPI()

# Initialize ChromaDB
chroma_api = API(Settings(
    chroma_db_impl="deta",
    deta_namespace=os.environ.get("DETA_NAME", "chroma-db"),
    deta_project_key=os.environ.get("DETA_PROJECT_KEY", "")
))
collection = chroma_api.create_collection(name="text_collection")

@app.post("/save_text")
def save_text(text: str):
    """
    Saves the given text to the ChromaDB database.
    """
    # Encode the text using a simple embedding function
    embedding = SimpleEmbeddingFunction()(text)

    # Add the text and its embedding to the ChromaDB collection
    collection.add(
        documents=[text],
        embeddings=[embedding]
    )

    return {"message": "Text saved successfully"}