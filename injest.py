import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

co = cohere.Client("Sk7RgtrSiuZ6yXEgLUeFN8pmJQPlkZ7fJEs8dA9r")
qdrant = QdrantClient(
    url="https://aff01812-01df-4ee6-b309-65409b708d26.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Zeu-g62NUPr56ulVN6A92f68Uo1XbzJhSyzKxGFeEn8",
)

collection_name = "humanoid_ai_book"

qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

texts = [
    "Chapter 1: Introduction to AI and Robotics",
    "Chapter 2: Humanoid Motion Control",
    "Chapter 3: Robot Simulations With Gazebo",
    "Chapter 4: NVIDIA Isaac Platform",
]

embeddings = co.embed(
    model="embed-english-v3.0",
    input_type="search_document",
    texts=texts
).embeddings

points = [
    PointStruct(id=i, vector=embeddings[i], payload={"text": texts[i]})
    for i in range(len(texts))
]

qdrant.upsert(collection_name=collection_name, points=points)

print("✅ Collection created and data uploaded.")