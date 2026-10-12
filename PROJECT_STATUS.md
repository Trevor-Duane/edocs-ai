# edocs-ai — Project Status

**Last updated:** 12 October 2026  
**Repository:** https://github.com/Trevor-Duane/edocs-ai  
**Primary branch:** `main`  
**Project status:** Active development

## 1. Project Overview

`edocs-ai` is a self-hosted AI sidecar designed to extend the eDocs+ document management system with intelligent document-processing and search capabilities.

The existing eDocs+ application remains the system of record for document storage, users, permissions, access control, and business workflows. `edocs-ai` provides AI-powered processing and retrieval without replacing those responsibilities.

### Primary objectives

- Automatically extract and classify incoming documents.
- Support OCR for scanned documents.
- Enable meaning-based document search.
- Identify duplicate and related documents.
- Answer staff questions using documents they are authorized to access.
- Support correspondence management and compliance monitoring.
- Produce management reports on document workloads and processing times.
- Preserve document references, page numbers, and relevant source information.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Python package and dependency management | uv |
| API framework | FastAPI |
| API server | Uvicorn |
| Database | PostgreSQL |
| Vector storage | pgvector |
| Database migrations | Alembic |
| Containerization | Docker and Docker Compose |
| PDF extraction | PyMuPDF |
| OCR | Tesseract OCR |
| Image processing | Pillow |
| OCR Python integration | pytesseract |
| Automated testing | pytest |
| Code quality | Ruff |
| Configuration | Environment variables and YAML files |

The Docker image uses Python 3.12. The host development environment has previously used Python 3.14, so Python-version differences should be considered when diagnosing dependency or test issues.

## 3. Repository Structure

The project uses a `src`-based Python package layout.

```text
edocs-ai/
├── alembic/
│   └── versions/
├── configs/
│   ├── entities/
│   └── models.yaml
├── deploy/
│   ├── backup/
│   ├── nginx/
│   └── systemd/
├── docs/
│   ├── api-contract.md
│   ├── architecture.md
│   └── runbook.md
├── scripts/
├── src/
│   └── edocs_ai/
│       ├── api/
│       │   └── v1/
│       ├── connectors/
│       │   └── edocs/
│       ├── core/
│       ├── db/
│       │   └── repositories/
│       ├── events/
│       ├── pipeline/
│       │   └── steps/
│       │       └── extractors/
│       ├── schemas/
│       ├── search/
│       ├── workers/
│       ├── main.py
│       └── settings.py
├── tests/
│   ├── fixtures/
│   ├── integration/
│   ├── unit/
│   └── golden/
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── README.md
└── PROJECT_STATUS.md
```

This structure describes the intended code organization. The presence of a module does not necessarily mean its full functionality is implemented or production-ready.

## 4. Infrastructure and Database

### Docker services

The project has a Docker Compose setup for the API and PostgreSQL.

Previously verified container names:

- API: `edocs-ai-api`
- PostgreSQL: `edocs-ai-postgres`

Previously configured ports:

- API: host port `8000`
- PostgreSQL: host port `5432`

The API container connects to PostgreSQL using the Compose service hostname, rather than `localhost`.

### Database

PostgreSQL uses the `pgvector/pgvector:pg16` image.

The initial Alembic migrations include:

- `e558bcdd012a` — enable pgvector.
- `44dae7fec956` — create initial AI tables.

Previously created tables:

- `documents`
- `document_chunks`
- `embeddings`
- `processing_jobs`
- `alembic_version`

The embeddings table was previously configured for 384-dimensional vectors. Confirm that the selected embedding model produces vectors of the expected dimension before implementing embedding generation.

### Environment configuration

The database configuration is intended to use `.env` variables:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

The `.env` file must remain local and must not be committed to GitHub. `.env.example` should document required variables using placeholders.

**Verification still required:** Confirm that the Compose configuration has been updated to reference these variables, `.env` is ignored by Git, and the containers start successfully with the updated configuration.

Changing a PostgreSQL environment variable does not automatically change credentials in an existing database volume.

## 5. Implemented and Verified Functionality

### API health check

The API health endpoint previously returned:

```json
{
  "status": "okay",
  "service": "eDocs AI",
  "version": "0.1.0",
  "environment": "development"
}
```

A database-backed document lookup endpoint was also previously tested.

### Document extraction

The extraction dispatcher supports:

- PDF files (`.pdf`)
- Word documents (`.docx`)
- Plain-text files (`.txt`)

The extraction result includes the source filename, file type, page count, extracted pages, full text, OCR status, and warnings.

### PDF OCR

PDF extraction uses PyMuPDF to extract selectable text. Pages with fewer than 20 characters are candidates for OCR.

For candidate pages, the extractor:

1. Renders the PDF page as an image.
2. Uses Pillow to open the image.
3. Invokes Tesseract through pytesseract.
4. Compares the OCR result with the original extracted text.
5. Retains the more useful result.
6. Reports warnings when OCR fails or the page still contains little extractable text.

Tesseract and its English language data have been installed in the Docker image.

**Real OCR smoke test passed.** An image-based PDF was processed inside Docker and returned:

```text
Pages: 1
OCR still needed: False
Extracted text: 'Page 1\nEDOCS OCR TEST 12345'
Warnings: []
```

This verifies the basic OCR integration. Accuracy on real, low-quality, multilingual, or complex government documents has not yet been established.

### Automated tests

Six extraction tests previously passed on the host:

1. PDF text extraction.
2. Plain-text extraction.
3. DOCX extraction.
4. Unsupported file format.
5. Missing file.
6. OCR fallback when a PDF page has no selectable text.

Previously reported result:

```text
6 passed in 0.35s
```

Run the tests again after subsequent changes to confirm the current state.

## 6. Git and GitHub

The project has been initialized as a Git repository.

- Default branch: `main`
- Remote: `origin`
- GitHub repository: https://github.com/Trevor-Duane/edocs-ai
- Initial push: successful
- Working tree: clean immediately after the initial push

Generated Python package metadata was identified for exclusion, and the Docker ignore file was identified for renaming to `.dockerignore`.

Verify the latest Git status before assuming all cleanup changes or later environment changes have been committed.

## 7. Security and Access Control

Security is a core requirement because eDocs+ may contain sensitive government correspondence.

Design principles:

- eDocs+ remains authoritative for user identities and document permissions.
- AI search and question-answering must enforce the original access-control rules.
- A document must not become accessible merely because it has been indexed or embedded.
- API credentials and database passwords must not be hardcoded in source files.
- `.env` files, private keys, and production credentials must never be committed.
- Logging and audit records should avoid exposing sensitive document contents.
- AI-generated answers should identify supporting sources wherever possible.
- Unsupported answers should be handled conservatively rather than fabricated.

These are architectural requirements; their implementation and testing must be verified before production use.

## 8. Planned Processing Pipeline

The intended document-processing flow is:

1. Receive a document event or discover a new document.
2. Validate document metadata and access-control information.
3. Extract text from PDF, DOCX, or TXT.
4. Apply OCR where necessary.
5. Classify the document.
6. Extract relevant entities and metadata.
7. Detect duplicates and related documents.
8. Split extracted text into chunks while preserving page references.
9. Generate embeddings.
10. Store document chunks and embeddings.
11. Make the document available to authorized semantic search.
12. Support retrieval-augmented question answering with source references.

The stages should be implemented incrementally, with tests and clear failure handling.

## 9. Recommended Next Milestones

### Milestone 1 — Repository and configuration hygiene

- Verify `.env` configuration in Docker Compose.
- Verify `.gitignore` and `.dockerignore`.
- Exclude generated files and secrets.
- Commit the project status document.
- Confirm a clean Git working tree.

### Milestone 2 — Harden document extraction

- Rerun extraction tests.
- Add tests for OCR failures and unreadable pages.
- Test empty PDFs and password-protected PDFs.
- Verify behavior for partially readable and mixed-content PDFs.
- Test OCR with representative documents.
- Confirm that failures produce useful warnings rather than silently losing content.

### Milestone 3 — Text normalization and chunking

- Define a consistent normalized-text format.
- Preserve page boundaries and source metadata.
- Implement configurable chunk size and overlap.
- Ensure chunks remain traceable to their source documents and pages.
- Add unit tests for empty content, short documents, long documents, and page boundaries.

### Milestone 4 — Embeddings and semantic retrieval

- Select an embedding model compatible with the 384-dimensional database column, or migrate the schema if a different dimension is required.
- Implement embedding generation.
- Persist embeddings and metadata.
- Implement similarity retrieval.
- Test retrieval with representative documents.

### Milestone 5 — Secure end-to-end processing

- Connect ingestion events to the processing pipeline.
- Add retry handling and job status tracking.
- Enforce document authorization at retrieval time.
- Implement source-grounded answers.
- Add integration tests for the complete flow.

## 10. Development Workflow

Run tests:

```bash
uv run pytest
```

Run lint checks:

```bash
uv run ruff check .
```

Validate Docker Compose configuration:

```bash
docker compose config --quiet
```

Check container status:

```bash
docker compose ps
```

Review local changes:

```bash
git status
git diff
```

Commit and push verified changes:

```bash
git add .
git commit -m "Describe the change"
git push
```

Never stage `.env`, credentials, private keys, database dumps, or other sensitive artifacts.

## 11. Working Agreement for Future Development

- Work in small, verifiable steps.
- Inspect existing code before changing it.
- Prefer focused changes over broad rewrites.
- Explain why a change is needed before introducing it.
- Run the relevant tests after each meaningful change.
- Distinguish implemented features from planned features.
- Verify behavior inside Docker when container-specific dependencies are involved.
- Update this file when the architecture, verified functionality, or next milestone changes.

## Current Next Action

**Begin Milestone 1 verification, then proceed to text normalization and document chunking.**

The immediate technical objective is to transform extracted document text into well-structured, page-aware chunks that can later be embedded and retrieved without losing source traceability.
