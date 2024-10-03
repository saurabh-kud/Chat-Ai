import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from app.config import QDRANT_HOST
from app.config import QDRANT_PORT


client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
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


def search_chunks(query_embeddings: any, limit: int = 10):
    return client.search(
        collection_name=COLLECTION_NAME, query_vector=query_embeddings, limit=limit
    )
