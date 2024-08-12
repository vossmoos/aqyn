import chromadb
import os

CHROMA_PATH = "customers/"

def init_tenant(tenant_id):
    customer_path = CHROMA_PATH+tenant_id
    chroma_client = chromadb.PersistentClient(path=customer_path)
    os.makedirs(customer_path, exist_ok=True)

    collection = chroma_client.create_collection(name=tenant_id)

    return collection

def get_documents(tenant_id):
    tenant_chroma_client = get_tenant_chroma_client(tenant_id)
    collection = tenant_chroma_client.get_collection(tenant_id)
    documents = collection.get()

    return documents

def get_collection(tenant_id):
    tenant_chroma_client = get_tenant_chroma_client(tenant_id)
    collection = tenant_chroma_client.get_collection(tenant_id)

    return collection

def get_tenant_chroma_client(tenant_id):
    customer_path = CHROMA_PATH+tenant_id
    chroma_client = chromadb.PersistentClient(path=customer_path)
    
    return chroma_client

def answer(collection, emb):
    documents = collection.query(
        query_embeddings=[emb],
        n_results=2
    )

    return documents