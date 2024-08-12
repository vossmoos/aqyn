import os
import base64
import json
from dotenv import load_dotenv
from firebase_admin import auth, credentials
from firebase_admin.exceptions import FirebaseError
from fastapi import APIRouter, status, HTTPException, Header, Body, Depends

def initialize_firebase():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the base64 encoded service account string
    encoded_service_account = os.getenv('GOOGLE_SERVICE_ACCOUNT')

    if not encoded_service_account:
        print("GOOGLE_SERVICE_ACCOUNT not found in environment variables.")
        return

    # Decode the base64 string
    decoded_bytes = base64.b64decode(encoded_service_account)
    service_account_info = json.loads(decoded_bytes)

    


def create_user(email, password):
    user = auth.create_user(
        email=email,
        password=password,
        email_verified=False
    )
    print(f'User created: {user.uid}')
    return user

def set_claim(uid: str):
    custom_claims = {"pool": "poc"}
    try:
        auth.set_custom_user_claims(uid, custom_claims)
    except ValueError as e:
        return e
    except FirebaseError as e:
        return e.args[0]
    
def check_auth_token(token):
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Authentication failed")
