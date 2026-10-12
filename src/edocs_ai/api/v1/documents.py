from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from edocs_ai.api.dependencies import get_db
from edocs_ai.db.repositories.documents import create_document, get_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/{document_id}")
def create_test_document(
    document_id: str,
    title: str,
    db: Session = Depends(get_db),
):
    document = create_document(
        db=db,
        document_id=document_id,
        title=title,
        mime_type="application/pdf",
    )

    return {
        "id": document.id,
        "title": document.title,
        "status": document.status,
    }


@router.get("/{document_id}")
def get_test_document(
    document_id: str,
    db: Session = Depends(get_db),
):
    document = get_document(db, document_id)

    if document is None:
        return {"error": "Document not found"}

    return {
        "id": document.id,
        "title": document.title,
        "status": document.status,
        "mime_type": document.mime_type,
    }