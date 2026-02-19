"""Extract text from a PDF and split into chunks for LLM processing."""

import json
import sys
from pathlib import Path

import fitz  # pymupdf


CHUNK_SIZE = 3000


def read_pdf(path: str) -> list[dict]:
    """Read a PDF and return a list of text chunks."""
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()

    chunks = []
    current = ""
    for paragraph in text.split("\n\n"):
        if len(current) + len(paragraph) > CHUNK_SIZE:
            if current.strip():
                chunks.append(current.strip())
            current = ""
        current += paragraph + "\n\n"
    if current.strip():
        chunks.append(current.strip())

    filename = Path(path).stem
    return [
        {"filename": filename, "chunk_index": i, "text": chunk}
        for i, chunk in enumerate(chunks)
    ]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/pdf_reader.py <path-to-pdf>", file=sys.stderr)
        sys.exit(1)

    result = read_pdf(sys.argv[1])
    print(json.dumps(result, indent=2))
