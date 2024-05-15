import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# prompt = PromptTemplate.from_template("You are a content creator. Write a technical blog about {topic}.")

# chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

# if __name__=="__main__":
#     topic = "vector databases"
#     resp = chain.invoke({"topic": topic})
#     print(resp)

# Define the prompt
prompt = "You are a content creator. Write a technical blog about 'how vector databases will impact the future of AI'."

response = llm.invoke(prompt)

print(response.content)