# ChunkSearch - JSON-based Document Search with BM25

A FastAPI-based backend application that allows you to upload JSON files containing document chunks and search through them using BM25 algorithm without requiring embeddings or LLMs.

## Features

- **JSON Upload**: Upload JSON files with document chunks and metadata
- **BM25 Search**: Semantic-like search using BM25 algorithm (no embeddings required)
- **Metadata Filtering**: Filter search results by file source, section labels, and other metadata
- **SQLite Storage**: Lightweight database storage for chunks
- **FastAPI Backend**: RESTful API with automatic documentation
- **CORS Enabled**: Ready for frontend integration

## Project Structure

```
ChunkSearch/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── db.py                # SQLite database operations
│   ├── models.py            # Pydantic models
│   ├── llama_indexer.py     # BM25 search implementation
│   └── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

## JSON Input Format

```json
{
  "success": true,
  "content_source_id": 1,
  "chunks": [
    {
      "file_source": "path/to/document.pdf",
      "label": "Section 1",
      "content": "The actual text content...",
      "page_number": 1,
      "created_at": "2024-01-01T12:00:00Z",
      "author": "John Doe",
      "category": "Technical",
      "tags": ["api", "documentation"]
    }
  ]
}
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ChunkSearch
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

The server will start at `http://127.0.0.1:8000`

## API Endpoints

### Upload JSON
- **POST** `/upload-json`
- Upload a JSON file containing document chunks
- File upload required

### Search Chunks
- **GET** `/search`
- Parameters:
  - `query` (required): Search query
  - `file_source` (optional): Filter by file source
  - `label` (optional): Filter by section label
  - `top_k` (optional): Number of results (default: 5)

### API Documentation
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Usage Examples

### Upload JSON File
```bash
curl -X POST "http://127.0.0.1:8000/upload-json" \
     -F "file=@your_document.json"
```

### Search for Content
```bash
curl "http://127.0.0.1:8000/search?query=ERP&top_k=3"
```

### Search with Metadata Filter
```bash
curl "http://127.0.0.1:8000/search?query=technology&file_source=report.pdf&label=Section%201"
```

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Search**: BM25 algorithm (rank-bm25)
- **Documentation**: Pydantic models
- **API Docs**: Swagger/OpenAPI

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE). 