import fbauth
import chroma
import gemini
import uuid
import firebase_admin

from fastapi import FastAPI, APIRouter, status, HTTPException, Header, Body, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from firebase_admin import credentials
from typing import Optional

app = FastAPI()
security = HTTPBearer()
MAX_DOCUMENTS=30
MAX_CHARS=5000

firebase_cred = credentials.Certificate("files/aqyn-427823-firebase-adminsdk-naz5w-8e3cdec27b.json")
default_app = firebase_admin.initialize_app(firebase_cred)

class Document(BaseModel):
    text: str

class Question(BaseModel):
    text: str
    tenant: str

class Tenant(BaseModel):
    email: str
    passw: str

@app.get("/")
async def root():
    return {"status":"ok"}

@app.get("/tenant")
async def get_tenant(authorization: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get a tenant.

    It returns a tenant by ID {id} with the following data:
    - Tenant documents

    """
    # get the tenant's collection
    decoded_token = fbauth.check_auth_token(authorization.credentials)
    collection = chroma.get_documents(decoded_token["uid"])

    return {"data": collection}

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
    
@app.post("/tenant/document")
async def post_doc(document: Document, authorization: HTTPAuthorizationCredentials = Depends(security)):
    """
    Insert a new document.

    Takes a document text from POST body

    """
    # document ID
    document_id = str(uuid.uuid4())
   # get the tenant's collection
    decoded_token = fbauth.check_auth_token(authorization.credentials)
    collection = chroma.get_collection(decoded_token["uid"])

    if (collection.count() > MAX_DOCUMENTS):
        raise HTTPException(
            status_code=403, 
            detail="Creation of an additional content element is not possible with the current plan"
        )

    # embed text document
    emb = gemini.get_embed(document.text[:MAX_CHARS])

    # save embeddings to chroma
    document = collection.add(
            documents=[document.text[:5000]],
            embeddings=[emb[0].values],
            ids=[document_id]
        )

    return document

@app.delete("/tenant/document/{document_id}", status_code=204)
async def delete_doc(document_id: str, authorization: HTTPAuthorizationCredentials = Depends(security)):
    """
    Index a document.

    """
    #get the tenant's collection
    decoded_token = fbauth.check_auth_token(authorization.credentials)
    collection = chroma.get_collection(decoded_token["uid"])

    collection.delete(
        ids=[document_id]
    )

    return {"status":"deleted"}

# Post a question
@app.post("/tenant/question")
async def ask_question(question: Question):
    """
    Ask a question to Aqyn

    """
    try:
        collection = chroma.get_collection(question.tenant)
        emb = gemini.get_embed(question.text[:MAX_CHARS])
        documents = chroma.answer(collection, emb[0].values)
        doc_string = ", ".join(documents["documents"][0])
        answer = gemini.get_content(doc_string, question.text[:MAX_CHARS])
        return {
            "question": question.text,
            "answer": answer,
            "docs": documents
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }