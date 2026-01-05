import os
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from backend.services.tutor import reload_notes
from fastapi import Depends

router = APIRouter(prefix="/admin", tags=["admin"])

ADMIN_KEY = os.getenv("ADMIN_KEY")

def verify_admin(x_admin_key: str | None):
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/status")
def admin_status(x_admin_key: str = Header(None)):
    verify_admin(x_admin_key)
    return {
        "status": "ok",
        "admin": True
    }


@router.post("/reload-notes")
def admin_reload_notes(x_admin_key: str = Header(None)):
    verify_admin(x_admin_key)
    try:
        return reload_notes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def admin_required(x_admin_key: str = Header(None)):
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/status", dependencies=[Depends(admin_required)])
def admin_status():
    return {"status": "ok", "admin": True}
