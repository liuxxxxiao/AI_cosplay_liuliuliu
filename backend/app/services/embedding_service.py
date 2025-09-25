# app/services/embedding_service.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from backend.app.config import EMBEDDING_MODEL

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
