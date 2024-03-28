import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up the LLM and prompt
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
prompt = PromptTemplate.from_template("You are a content creator. Write a technical blog about {topic}.")
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# Set up ChromaDB and embedding function
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=GOOGLE_API_KEY)
client = chromadb.Client()
collection = client.create_collection(name="personal_text_db", embedding_function=google_ef)

if __name__ == "__main__":
    topic = "vector databases"
    resp = chain.invoke({"topic": topic})

    # Save personal text to ChromaDB
    personal_text = "Your personal text here"
    embedding = google_ef([personal_text])[0]
    collection.add(documents=[personal_text], embeddings=[embedding], ids=[f"doc_0"])

    # Retrieve text from ChromaDB
    retrieved_doc = collection.query(query_texts=[personal_text], n_results=1)
    print(retrieved_doc["documents"][0])