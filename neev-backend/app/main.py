"""
NEEV - FastAPI minimal API
- /health : quick health check
- /search : returns top-k NCO matches (dummy for now; we’ll wire real search next)
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="NEEV API", version="0.1.0")

class SearchRequest(BaseModel):
    query: str
    language: str = "en"
    k: int = 5

class SearchResult(BaseModel):
    code: str
    title: str
    confidence: float
    hierarchy: Dict[str, str]
    explanation: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/search", response_model=List[SearchResult])
def search(req: SearchRequest):
    # Temporary stub result
    return [
        {
            "code": "75330100",
            "title": "Sewing Machine Operator",
            "confidence": 0.83,
            "hierarchy": {
                "major_group": "75",
                "sub_major_group": "7533",
                "minor_group": "753301",
                "unit_group": "75330100"
            },
            "explanation": "Matched on 'sewing', 'machine', 'operator'; semantic similarity high."
        }
    ]
