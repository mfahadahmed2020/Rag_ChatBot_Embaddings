import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Initialize Cohere client
cohere_client = cohere.Client("Sk7RgtrSiuZ6yXEgLUeFN8pmJQPlkZ7fJEs8dA9r")
EMBED_MODEL = "embed-english-v3.0"

# Connect to Qdrant Cloud
qdrant_client = QdrantClient(
    url="https://aff01812-01df-4ee6-b309-65409b708d26.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Zeu-g62NUPr56ulVN6A92f68Uo1XbzJhSyzKxGFeEn8",
)

def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts = [
    "Chapter 1: Introduction to AI and Robotics",
    "Chapter 2: Humanoid Motion Control",
    "Chapter 3: Robot Simulations With Gazebo",
    "Chapter 4: NVIDIA Isaac Platform",
    ],
        )
    return response.embeddings[0]

def retrieve(query):
    embedding = get_embedding(query)
    results = qdrant_client.query_points(
        collection_name="humanoid_ai_book",
        query=embedding,
        limit=5,
    )
    return [point.payload["text"] for point in results.points]

print(retrieve("What data do you have?"))