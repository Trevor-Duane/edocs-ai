
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import pymupdf
import pytesseract
from PIL import Image


# Pages with fewer characters than this are candidates for OCR.
OCR_MIN_TEXT_CHARS = 20


@dataclass
class ExtractedPage:
    page_number: int
    text: str


@dataclass
class ExtractionResult:
    source: str
    file_type: str
    page_count: int
    pages: list[ExtractedPage]
    full_text: str
    needs_ocr: bool
    warnings: list[str] | None = None


def _run_ocr(page: pymupdf.Page) -> str:
    """Render a PDF page as an image and recognize its text with Tesseract."""
    pixmap = page.get_pixmap(
        matrix=pymupdf.Matrix(2, 2),
        alpha=False,
    )

    image_bytes = pixmap.tobytes("png")

    with Image.open(BytesIO(image_bytes)) as image:
        return pytesseract.image_to_string(
            image,
            lang="eng",
        ).strip()


def extract_pdf(file_path: str | Path) -> ExtractionResult:
    """
    Extract text from a PDF, using OCR when a page has little
    or no selectable text.

    Page numbers are preserved. OCR failures are reported as warnings.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    pages: list[ExtractedPage] = []
    warnings: list[str] = []
    needs_ocr = False

    with pymupdf.open(path) as pdf:
        if pdf.is_encrypted and not pdf.authenticate(""):
            raise ValueError("PDF is password-protected and cannot be opened.")

        for index, page in enumerate(pdf):
            page_number = index + 1
            text = page.get_text("text").strip()

            # Only run OCR on pages with little or no selectable text.
            if len(text) < OCR_MIN_TEXT_CHARS:
                try:
                    ocr_text = _run_ocr(page)

                    # Keep whichever extraction produced more text.
                    if len(ocr_text) > len(text):
                        text = ocr_text

                    if len(text) < OCR_MIN_TEXT_CHARS:
                        needs_ocr = True
                        warnings.append(
                            f"Page {page_number} still has little or no "
                            "extractable text after OCR."
                        )

                except Exception as exc:
                    needs_ocr = True
                    warnings.append(
                        f"OCR failed on page {page_number}: "
                        f"{type(exc).__name__}: {exc}"
                    )

            pages.append(
                ExtractedPage(
                    page_number=page_number,
                    text=text,
                )
            )

    full_text = "\n\n".join(
        f"Page {page.page_number}\n{page.text}"
        for page in pages
        if page.text
    )

    return ExtractionResult(
        source=path.name,
        file_type=".pdf",
        page_count=len(pages),
        pages=pages,
        full_text=full_text,
        needs_ocr=needs_ocr,
        warnings=warnings,
    )
