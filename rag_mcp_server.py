from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
import os
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
    google_api_key=GEMINI_API_KEY
)

chat_model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)

# Chunking the data for storing in vector db
file = "sample.pdf"
data = PyPDFLoader(file_path=file).load()

text_splitter_config = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunked_data = text_splitter_config.split_documents(data)

vector_db = Chroma.from_documents(documents=chunked_data, embedding=embeddings_model)

qa = RetrievalQA.from_chain_type(llm=chat_model, retriever=vector_db.as_retriever())

mcp = FastMCP("RAG_MCP_SERVER")

@mcp.tool()
def retrieve_answer(prompt):
    return qa.invoke(prompt)
    
if __name__ == '__main__':
    mcp.run(transport="streamable-http")