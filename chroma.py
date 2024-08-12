import chromadb
import os

CHROMA_PATH = "customers/"

def init_tenant(tenant_id):
    customer_path = CHROMA_PATH+tenant_id
    chroma_client = chromadb.PersistentClient(path=customer_path)
    os.makedirs(customer_path, exist_ok=True)

    collection = chroma_client.create_collection(name=tenant_id)

    return collection