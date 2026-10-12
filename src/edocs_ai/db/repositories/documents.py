from sqlalchemy import select
from sqlalchemy.orm import Session

from edocs_ai.db.models import Document


def create_document(
    db: Session,
    document_id: str,
    title: str,
    mime_type: str | None = None,
    storage_url: str | None = None,
) -> Document:
    document = Document(
        id=document_id,
        title=title,
        mime_type=mime_type,
        storage_url=storage_url,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_document(db: Session, document_id: str) -> Document | None:
    statement = select(Document).where(Document.id == document_id)
    return db.scalar(statement)