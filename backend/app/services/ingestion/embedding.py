import os
from sentence_transformers import SentenceTransformer  # type: ignore
from typing import List


DOCUMENT_ENCODER_MODEL = (
    os.environ.get("DOCUMENT_ENCODER_MODEL") or "thenlper/gte-small"
)

# If the below is changed, Vespa deployment must also be changed
DOC_EMBEDDING_DIM = 384
# Model should be chosen with 512 context size, ideally don't change this
DOC_EMBEDDING_CONTEXT_SIZE = 512
NORMALIZE_EMBEDDINGS = (
    os.environ.get("NORMALIZE_EMBEDDINGS") or "False"
).lower() == "true"

_EMBED_MODEL: None | SentenceTransformer = None


def get_local_embedding_model(
    model_name: str = DOCUMENT_ENCODER_MODEL,
    max_context_length: int = DOC_EMBEDDING_CONTEXT_SIZE,
) -> SentenceTransformer:
    global _EMBED_MODEL
    if _EMBED_MODEL is None or max_context_length != _EMBED_MODEL.max_seq_length:
        # logger.info(f"Loading {model_name}")
        _EMBED_MODEL = SentenceTransformer(model_name)
        _EMBED_MODEL.max_seq_length = max_context_length
    return _EMBED_MODEL


class EmbeddingModel:
    def __init__(
        self,
        model_name: str = DOCUMENT_ENCODER_MODEL,
        max_seq_length: int = DOC_EMBEDDING_CONTEXT_SIZE,
    ) -> None:
        self.model_name = model_name
        self.max_seq_length = max_seq_length

    def load_model(self) -> SentenceTransformer | None:

        return get_local_embedding_model(
            model_name=self.model_name, max_context_length=self.max_seq_length
        )

    def encode(
        self, texts: str, normalize_embeddings: bool = NORMALIZE_EMBEDDINGS
    ) -> list[list[float]]:

        local_model = self.load_model()

        if local_model is None:
            raise RuntimeError("Failed to load local Embedding Model")

        return local_model.encode(
            texts, normalize_embeddings=normalize_embeddings
        ).tolist()


class CustomCacheEmbedding:
    def __init__(self):
        self.embedding_model = EmbeddingModel()

    def embed_documents(self, texts: str) -> List[List[float]]:
        return self.embedding_model.encode(texts=texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
