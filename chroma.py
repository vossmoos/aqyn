import chromadb
import os

CHROMA_PATH = "customers/"
MAX_DOCUMENTS=3
MAX_DISTANCE=1.1

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
        n_results=MAX_DOCUMENTS
    )

    return filter_docs_by_distance(documents)

def filter_docs_by_distance(docs, max_distance=MAX_DISTANCE):
    # Initialize lists to store the filtered data
    filtered_ids = []
    filtered_distances = []
    filtered_metadatas = []
    filtered_documents = []

    # Iterate over the distances and associated data
    for i, distance in enumerate(docs['distances'][0]):
        if distance <= max_distance:
            filtered_ids.append(docs['ids'][0][i])
            filtered_distances.append(distance)
            filtered_metadatas.append(docs['metadatas'][0][i])
            filtered_documents.append(docs['documents'][0][i])

    # Update the original docs structure with the filtered lists
    docs['ids'][0] = filtered_ids
    docs['distances'][0] = filtered_distances
    docs['metadatas'][0] = filtered_metadatas
    docs['documents'][0] = filtered_documents

    return docs