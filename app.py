import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from validator import validate, load_brand_config

API_TOKEN = os.getenv("VALIDATOR_TOKEN", None)

app = FastAPI(title="Multi-Brand GPT Validator", version="1.0.0")

class Link(BaseModel):
    url: str
    utm: bool = True

class MediaSuggestion(BaseModel):
    type: str
    count: Optional[int] = None
    notes: Optional[str] = None

class ValidateRequest(BaseModel):
    brand: str = Field(..., examples=["Amar"])
    platform: str = Field(..., examples=["Instagram"])
    caption: str
    hashtags: List[str] = []
    cta: Optional[str] = None
    media_suggestion: MediaSuggestion
    links: List[Link] = []
    week: Optional[str] = None
    post_id: Optional[str] = None

def _auth_check(authorization: Optional[str]):
    if not API_TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/banks/{brand}")
def banks(brand: str, authorization: Optional[str] = Header(None)):
    _auth_check(authorization)
    try:
        cfg = load_brand_config(brand)
        return {"brand": brand, "keys": list(cfg.keys())}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/validate")
def do_validate(req: ValidateRequest, authorization: Optional[str] = Header(None)):
    _auth_check(authorization)
    ok, errors, payload = validate(req.model_dump())
    if not ok:
        return {"valid": False, "errors": errors, "suggestions": {}}
    return {"valid": True, **payload}
