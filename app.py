import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from validator import validate, load_brand_config
from google_sheets_service import sheets_service
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

@app.get("/debug")
def debug():
    import os
    return {
        "current_dir": os.getcwd(),
        "files": os.listdir("."),
        "config_exists": os.path.exists("config"),
        "config_files": os.listdir("config") if os.path.exists("config") else "No config dir"
    }

@app.get("/banks/{brand}")
def banks(brand: str, authorization: Optional[str] = Header(None)):
    _auth_check(authorization)
    try:
        cfg = load_brand_config(brand)
        return {"brand": brand, "keys": list(cfg.keys())}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/brands")
def get_brands(authorization: Optional[str] = Header(None)):
    _auth_check(authorization)
    import os
    import json
    
    brands = []
    config_dir = "config"
    
    if os.path.exists(config_dir):
        for file in os.listdir(config_dir):
            if file.endswith('.json') and file != 'multibrand.json':
                brand_name = file.replace('.json', '').replace('_', ' ').title()
                try:
                    with open(os.path.join(config_dir, file), 'r') as f:
                        cfg = json.load(f)
                        brands.append({
                            "name": cfg.get("brand", brand_name),
                            "voice": cfg.get("voice", {}),
                            "story": cfg.get("story", ""),
                            "platforms": cfg.get("platforms", []),
                            "hashtag_banks": cfg.get("hashtag_bank", {}),
                            "cta_banks": cfg.get("cta_bank", {}),
                            "media_policy": cfg.get("media_policy", {}),
                            "forbidden_words": cfg.get("forbidden_words", []),
                            "allowed_domains": cfg.get("link_policy", {}).get("allowed_domains", [])
                        })
                except Exception as e:
                    continue
    
    return {"brands": brands}

@app.get("/brands/{brand}")
def get_brand_info(brand: str, authorization: Optional[str] = Header(None)):
    _auth_check(authorization)
    try:
        cfg = load_brand_config(brand)
        return {
            "brand": cfg.get("brand", brand),
            "voice": cfg.get("voice", {}),
            "story": cfg.get("story", ""),
            "platforms": cfg.get("platforms", []),
            "hashtag_banks": cfg.get("hashtag_bank", {}),
            "cta_banks": cfg.get("cta_bank", {}),
            "media_policy": cfg.get("media_policy", {}),
            "forbidden_words": cfg.get("forbidden_words", []),
            "allowed_domains": cfg.get("link_policy", {}).get("allowed_domains", []),
            "required_disclosures": cfg.get("required_disclosures", [])
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/validate")
def do_validate(req: ValidateRequest, authorization: Optional[str] = Header(None)):
    try:
        _auth_check(authorization)
        ok, errors, payload = validate(req.model_dump())
        if not ok:
            return {"valid": False, "errors": errors, "suggestions": {}}
        return {"valid": True, **payload}
    except Exception as e:
        return {"error": str(e), "type": type(e).__name__}
