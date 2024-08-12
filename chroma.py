import chromadb

CHROMA_PATH = "customers/"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

def init_tenant():

    return 