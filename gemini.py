import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel

def get_embed(content):
    credentials = service_account.Credentials.from_service_account_file("files/aqyn-427823-firebase-adminsdk-naz5w-8e3cdec27b.json")
    vertexai.init(credentials=credentials, project="aqyn-427823", location="europe-west4")
    embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    vector = embedding_model.get_embeddings([content])
        
    return vector[0].values