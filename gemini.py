import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel

vertexai.init(project="aqyn-427823", location="europe-west4")
credentials = service_account.Credentials.from_service_account_file("files/aqyn-427823-firebase-adminsdk-naz5w-8e3cdec27b.json")
embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

def get_embed(content):
    vector = embedding_model.get_embeddings([content])
        
    return vector[0].values