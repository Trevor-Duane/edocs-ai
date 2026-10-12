
from pathlib import Path

from edocs_ai.pipeline.steps.extractors.pdf import (
    ExtractedPage,
    ExtractionResult,
)


def extract_txt(file_path: str | Path) -> ExtractionResult:
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Text file not found: {path}")

    # UTF-8 first; replace invalid byte sequences instead of crashing.
    full_text = path.read_text(encoding="utf-8", errors="replace").strip()

    warnings = []
    if "\ufffd" in full_text:
        warnings.append("Some characters could not be decoded as UTF-8.")

    if not full_text:
        warnings.append("The text file is empty.")

    return ExtractionResult(
        source=path.name,
        file_type=".txt",
        page_count=0,
        pages=[ExtractedPage(page_number=0, text=full_text)],
        full_text=full_text,
        needs_ocr=False,
        warnings=warnings,
    )
