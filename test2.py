import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from chromadb import ChromaDB
import chromadb



load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

prompt = PromptTemplate.from_template("You are a content creator. Write a technical blog about {topic}.")

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# Initialize ChromaDB
db = chromadb.ChromaDB("personal_text_db")

if __name__ == "__main__":
    topic = "vector databases"
    resp = chain.invoke({"topic": topic})
    
    # Save personal text to ChromaDB
    personal_text = "Your personal text here"
    db.save_vector(personal_text, resp)
    
    # Retrieve text from ChromaDB for conversation
    retrieved_text = db.retrieve_nearest(personal_text)
    print(retrieved_text)