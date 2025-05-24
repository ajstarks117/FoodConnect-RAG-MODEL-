from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer

def load_documents(file_path):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    return documents

def split_documents(documents):
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

def get_vectorstore(documents):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents, embedding_model, persist_directory="db")
    return vectorstore
