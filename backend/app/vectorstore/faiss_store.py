# app/vectorstore/faiss_store.py
import os
from langchain_community.vectorstores import FAISS
from backend.app.services.embedding_service import get_embedding_model
from backend.app.config import VECTOR_DB_PATH

def get_faiss_store():
    if os.path.exists(VECTOR_DB_PATH):
        return FAISS.load_local(VECTOR_DB_PATH, get_embedding_model(), allow_dangerous_deserialization=True)
    else:
        return None

def save_faiss_store(store):
    store.save_local(VECTOR_DB_PATH)

def add_document_to_store(text):
    embedding_model = get_embedding_model()
    store = get_faiss_store()

    if not store:
        store = FAISS.from_texts([text], embedding_model)
    else:
        store.add_texts([text])

    save_faiss_store(store)
    return store


