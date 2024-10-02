import os
from pathlib import Path

from fastapi import UploadFile, HTTPException
from app.services.ingestion.file_utils import extract_text_from_csv
from app.services.ingestion.file_utils import extract_text_from_pdf
from app.services.ingestion.file_utils import extract_text_from_txt
from app.services.ingestion.file_utils import extract_text_from_docx
from app.services.ingestion.file_utils import create_metadata
from app.services.ingestion.chunking import chunk_content
from app.services.ingestion.chunking import csv_chunking
from app.services.ingestion.embedding import CustomCacheEmbedding
from app.services.ingestion.indexing import insert_vectors
from app.services.ingestion.indexing import ensure_collection_exists

_VALID_FILE_EXTENSIONS = [
    ".txt",
    ".pdf",
    ".docx",
    ".doc",
    ".xlsx",
    ".csv",
]


def get_file_ext(file_path_or_name: str | Path) -> str:
    _, extension = os.path.splitext(file_path_or_name)
    return extension.lower()


# Define the base path
base_path = Path.cwd() / "uploaded_files"  # Main directory with "uploaded_files"


def file_processing(file: UploadFile) -> str:

    try:
        extention = get_file_ext(file.filename)

        if extention not in _VALID_FILE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension for file: '{file.filename}'. Must be one of {_VALID_FILE_EXTENSIONS}",
            )

        file_location = Path(base_path)
        os.makedirs(file_location, exist_ok=True)

        file_path = file_location / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        content = ""
        chunks = []
        if extention == ".pdf":
            content = extract_text_from_pdf(file_path=file_path)
        elif extention == ".docx":
            content = extract_text_from_docx(file_path=file_path)
        elif extention == ".csv":
            content = extract_text_from_csv(file_path=file_path)
        elif extention == ".txt":
            content = extract_text_from_txt(file_path=file_path)

        if extention != ".csv":
            chunks = chunk_content(content=content)
        else:
            chunks = csv_chunking(content=content)

        metadata = create_metadata(document_title=file.filename, source_type=extention)

        model = CustomCacheEmbedding()
        ensure_collection_exists()

        for index, chunks_str in enumerate(chunks):
            embeddings = model.embed_documents(chunks_str)
            insert_vectors(
                chunk=chunks_str,
                metadata=metadata,
                chunk_id=index,
                embeddings=embeddings,
            )

        return file_path
    except Exception as e:
        HTTPException(status_code=500, detail=f"Error while indexing the file {str(e)}")
