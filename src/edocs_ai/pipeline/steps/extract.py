
from pathlib import Path

from edocs_ai.pipeline.steps.extractors.pdf import extract_pdf
from edocs_ai.pipeline.steps.extractors.text import extract_txt
from edocs_ai.pipeline.steps.extractors.word import extract_docx


SUPPORTED_EXTENSIONS = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".txt": extract_txt,
}


def extract_document(file_path: str | Path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    extractor = SUPPORTED_EXTENSIONS.get(path.suffix.lower())

    if extractor is None:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported document format: {path.suffix or '(no extension)'}. "
            f"Supported formats: {supported}"
        )

    return extractor(path)
