from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

import os
load_dotenv()
print(os.getenv("USER_AGENT"))


urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

# embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",     
    model_kwargs={'device': 'cpu'},         
    encode_kwargs={'normalize_embeddings': True}  
)

# vectorstore = Chroma.from_documents(
#     documents=doc_splits,
#     collection_name="rag-chroma",
#     embedding=embeddings,
#     persist_directory="./.chroma-google",
# )

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma-google",
    embedding_function=embeddings,
).as_retriever()
