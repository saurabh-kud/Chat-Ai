from llama_index.core.node_parser import SentenceSplitter
import os
from transformers import AutoTokenizer  # type: ignore

_TOKENIZER: None | AutoTokenizer = None


def get_default_tokenizer() -> AutoTokenizer:
    global _TOKENIZER
    if _TOKENIZER is None:
        _TOKENIZER = AutoTokenizer.from_pretrained("thenlper/gte-small")
        if hasattr(_TOKENIZER, "is_fast") and _TOKENIZER.is_fast:
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
    return _TOKENIZER


def chunk_content(content: str):

    try:
        tokenizer = get_default_tokenizer()
        sentence_aware_splitter = SentenceSplitter(
            tokenizer=tokenizer.tokenize, chunk_size=512, chunk_overlap=0
        )
        chunks = sentence_aware_splitter.split_text(content)
        return chunks
    except Exception as e:
        print(str(e))


def csv_chunking(content) -> list[str]:
    print("you are here")
    print(content)
    tokenizer = get_default_tokenizer()
    sentence_aware_splitter = SentenceSplitter(
        tokenizer=tokenizer.tokenize, chunk_size=512, chunk_overlap=0
    )
    header = content.get("header_str", "")
    batches = content.get("batch", [])
    chunks = []
    for batch in batches:
        print(batch)

        split_texts = sentence_aware_splitter.split_text(batch)

        for index, chunk_str in enumerate(split_texts):
            print(header + "\n" + chunk_str)
            chunks.append(header + "\n" + chunk_str)

    return chunks
