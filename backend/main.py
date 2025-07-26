from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import json
import db
from models import UploadJSONModel
from llama_indexer import bm25_index

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    db.create_table()
    bm25_index.build_index()

@app.post("/upload-json")
def upload_json(file: UploadFile = File(...)):
    try:
        data = json.load(file.file)
        upload_model = UploadJSONModel(**data)
        for chunk in upload_model.chunks:
            db.insert_chunk(chunk.dict())
        bm25_index.build_index()
        return {"message": "Chunks uploaded and indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/search")
def search(
    query: str = Query(...),
    file_source: Optional[str] = Query(None),
    label: Optional[str] = Query(None),
    top_k: int = Query(5)
):
    metadata_filter = {}
    if file_source:
        metadata_filter['file_source'] = file_source
    if label:
        metadata_filter['label'] = label
    results = bm25_index.search(query, metadata_filter=metadata_filter, top_k=top_k)
    return {"results": results} 