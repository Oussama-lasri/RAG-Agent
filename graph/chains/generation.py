
from dotenv import load_dotenv
load_dotenv()
from langsmith import Client
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pprint import pprint

llm = ChatOpenAI(temperature=0)
client = Client()
prompt = client.pull_prompt("rlm/rag-prompt")
pprint(prompt)
generation_chain = prompt | llm | StrOutputParser()







