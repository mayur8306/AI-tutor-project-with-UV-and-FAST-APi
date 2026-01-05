from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"status": "OK"}

@router.get("/meta/config")
def meta_config():
    return {
        "service": "C/Python Tutor",
        "model": "llama-3.1-8b-instant",
        "languages": ["c", "python"],
        "default_language": "c",
        "version": "0.1"
    }
