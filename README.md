# Document Relevance Highlighter

A standalone FastAPI service that takes two PDFs — a **context document** and a
**target document** — and returns the target document with sections visually
highlighted according to how relevant they are to the context.

Originally scoped for resume/job-description matching, but generalized to work
with any context/target document pair (e.g. a spec vs. a report, a policy doc
vs. a contract).

## How it works

1. Both PDFs are uploaded to a single endpoint.
2. Text (and, for the target document, position data) is extracted from each.
3. The context document is chunked into reference points (paragraphs/sentences).
4. The target document is chunked into spans (lines/sentences) with position
   data preserved.
5. Every target span is embedded and compared against every context chunk
   using cosine similarity, producing a relevance score per span.
6. Scores are mapped onto a highlight intensity scale (stronger match =
   stronger highlight).
7. Highlights are drawn directly onto the target PDF at each span's original
   position, and the annotated PDF is returned.

## API

### `POST /highlight`

**Request:** `multipart/form-data`

| Field              | Type | Description                              |
|--------------------|------|-------------------------------------------|
| `context_document` | PDF  | Sets the relevance context                |
| `target_document`  | PDF  | Document to be marked up                  |

**Response:** `application/pdf` — the target document with highlight overlays,
opacity/color scaled by similarity score.

## Project structure

```
resume-highlighter/
├── app/
│   ├── main.py              # FastAPI app + /highlight endpoint
│   ├── extraction.py        # PDF text + position extraction
│   ├── chunking.py          # Context + target chunking
│   ├── scoring.py           # Embedding + cosine similarity
│   ├── highlighting.py      # Score-to-color mapping + PDF annotation
│   └── models.py            # Pydantic models / shared types
├── tests/
│   ├── test_extraction.py
│   ├── test_scoring.py
│   └── fixtures/            # Sample PDF pairs for testing
├── requirements.txt
├── .env                      # Config: thresholds, model name, etc.
└── README.md
```

Each module maps to one stage of the build (see Roadmap below), so stages can
be built and tested independently before being wired together.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Once running, open `http://127.0.0.1:8000/docs` for an interactive upload form
(FastAPI's auto-generated Swagger UI) to test the endpoint manually.

## Dependencies

- `fastapi`, `uvicorn[standard]`, `python-multipart`, `pydantic` — API layer
- `pymupdf` — PDF text/position extraction and highlight rendering
- `sentence-transformers` — embedding model for similarity scoring (default:
  `all-MiniLM-L6-v2`)

## Known limitations

- Scanned/image-based PDFs are not supported — text extraction requires PDFs
  with an actual text layer. OCR would need to be added separately for those.
- Multi-column layouts or tables may scramble reading order during text
  extraction; not yet handled.
