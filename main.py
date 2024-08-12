import fbauth
import chroma
import firebase_admin

from fastapi import FastAPI
from pydantic import BaseModel
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from firebase_admin import credentials

app = FastAPI()

firebase_cred = credentials.Certificate("files/aqyn-427823-firebase-adminsdk-naz5w-8e3cdec27b.json")
default_app = firebase_admin.initialize_app(firebase_cred)

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

# Create a tenant
@app.post("/tenant/")
async def tenant(tenant: Tenant):
    """
    Register a tenant.

    This endpoint allows you to create a new tenant. It includes the following:
    - Create a Firebase User *
    - Create a chromadb database.
    - Create a chromadb collection.

    """
    try:
        user = fbauth.create_user(tenant.email, tenant.passw)
        fbauth.set_claim(user.uid)
        chroma.init_tenant(user.uid)
        return {
            "status": "tenant created",
            "uid": user.uid
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
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