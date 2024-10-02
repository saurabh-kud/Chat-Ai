import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams


qdrant_host = "localhost"
qdrant_port = 6333


client = QdrantClient(host=qdrant_host, port=qdrant_port)
COLLECTION_NAME = "chat-ai"
VECTOR_SIZE = 384


def ensure_collection_exists():
    collections = client.get_collections().collections
    if not any(collection.name == COLLECTION_NAME for collection in collections):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def insert_vectors(chunk: str, metadata: dict, chunk_id: int, embeddings: list):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings,
                payload={
                    "document_id": metadata["document_id"],
                    "chunk_id": chunk_id,
                    "title": metadata.get("title", ""),
                    "content": chunk,
                    "metadata": metadata,
                },
            )
        ],
    )
