from PyPDF2 import PdfReader
from fastapi import HTTPException
import docx
import csv
import time
import uuid


def extract_text_from_csv(file_path: str):
    """Extract text from a CSV file."""
    header_str = ""
    result = []
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        try:
            csvreader = csv.reader(file, delimiter=",", quotechar='"')
            headers = next(csvreader)
            header_str = ",".join(headers)

            batch = []
            for row in csvreader:
                batch.append(row)
                if len(batch) == 10:
                    batch_str = "\n".join(",".join(r) for r in batch)
                    result.append(batch_str)
                    batch[:] = []

            # Add the remaining rows if they exist
            if batch:
                batch_str = "\n".join(",".join(r) for r in batch)
                result.append(batch_str)
        except Exception as e:
            # logger.error(f"Failed to read  DOC '{file_name}': {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to read CSV '{file_path}'"
            )

    return {"header_str": header_str, "batch": result}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_txt(file_path: str) -> str:
    """Extract text from a TXT file."""
    with open(file_path, "r") as f:
        return f.read()


def create_metadata(
    document_title,
    source_type,
):
    return {
        "document_id": str(uuid.uuid4()),
        "semantic_identifier": document_title,
        "title": document_title,
        "source_type": source_type,
        "doc_updated_at": time.time(),
    }
