import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel

GCP_PROJECT="aqyn-427823"
GCP_REGION="europe-west4"

def get_embed(content):
    credentials = service_account.Credentials.from_service_account_file("files/aqyn-427823-firebase-adminsdk-naz5w-8e3cdec27b.json")
    vertexai.init(credentials=credentials, project=GCP_PROJECT, location=GCP_REGION)
    embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    vector = embedding_model.get_embeddings([content])
        
    return vector

def get_content(document, question):
    # Set up GCP service account authentication
    credentials = service_account.Credentials.from_service_account_file("files/aqyn-427823-firebase-adminsdk-naz5w-8e3cdec27b.json")

    # Initialize the AI Platform client
    vertexai.init(credentials=credentials, project=GCP_PROJECT, location=GCP_REGION)

    content_model = GenerativeModel("gemini-1.5-pro")

    # Create the prompt
    prompt = f"""
    You are a professional Product Specialist. About the product you know the following given information: {document}, please answer to the following
    customer question: {question}. For your answer use strictly the given information as a knowledge base.
    """

    # Generate content using the model
    response = content_model.generate_content(prompt)

    return response.text      
    return ""