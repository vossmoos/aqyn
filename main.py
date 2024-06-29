from fastapi import FastAPI
from pydantic import BaseModel
import firebase

app = FastAPI()

class Document(BaseModel):
    text: str

class Question(BaseModel):
    text: str

class Tenant(BaseModel):
    email: str
    passw: str

@app.get("/")
async def root():
    return {"status":"ok"}

@app.get("/tenant/{id}")
async def get_tenant(id: int):
    """
    Get a tenant.

    It returns a tenant by ID {id} with the following data:
    - Tenant name
    - Tenant email
    - Tenant JS Widget
    - Tenant Slug

    """
    return {"status":"tenant GET"}

@app.get("/tenant/{id}/documents/{limit}/{offset}")
async def get_docs(id: int, limit: int, offset: int):
    """
    Get all documents with limit and offset.

    It returns a tenant by ID {id} with the following data:
    - Tenant name
    - Tenant email
    - Tenant JS Widget
    - Tenant Slug

    """
    return {"status":"documents GET"}

@app.get("/tenant/{id}/questions/{limit}/{offset}")
async def get_questions(id: int, limit: int, offset: int):
    """
    Update an existent document.

    Takes a document text from POST body

    """
    #print(f"Received document for tenant {id} and document ID {docid}: {document.text}")
    #print(document)

    return {"status":"questions GET"}

# Create a 
@app.post("/tenant/")
async def tenant(tenant: Tenant):
    """
    Register a tenant.

    This endpoint allows you to create a new tenant. It includes the following:
    - Create a Firebase User
    - Create a datastax astradb workspace.
    - Create an astradb collection.
    - Create a document in default collection with the tenant

    """
    firebase.initialize_firebase()
    print(tenant)

    return {"status":"tenant created"}

@app.post("/tenant/{id}/documents")
async def post_doc(id: int, document: Document):
    """
    Insert a new document.

    Takes a document text from POST body

    """
    #print(f"Received document for tenant {id} and document ID {docid}: {document.text}")
    #print(document)

    return {"status":document.text}

@app.put("/tenant/{id}/documents/{docid}")
async def update_doc(id: int, docid: int, document: Document):
    """
    Update an existent document.

    Takes a document text from POST body

    """
    #print(f"Received document for tenant {id} and document ID {docid}: {document.text}")
    #print(document)

    return {"status":document.text}

@app.post("/tenant/{id}/question")
async def post_question(id: int, question: Question):
    """
    Insert a new document.

    Takes a document text from POST body

    """
    #print(f"Received document for tenant {id} and document ID {docid}: {document.text}")
    #print(document)

    return {"status":question.text}

@app.post("/tenant/{id}/document/{qid}/index")
async def index_doc(id: int, qid: int):
    """
    Index a document.

    """
    #print(f"Received document for tenant {id} and document ID {docid}: {document.text}")
    #print(document)

    return {"status":"indexed"}