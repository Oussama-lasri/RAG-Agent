
from dotenv import load_dotenv
load_dotenv()
from langsmith import Client
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pprint import pprint

# llm = ChatOpenAI(temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview",version="v1", temperature=0)
client = Client()
prompt = client.pull_prompt("rlm/rag-prompt")
# print(f"from generation " + prompt)
generation_chain = prompt | llm | StrOutputParser()







