from fastapi import FastAPI,Request
from backend.routes import chat, meta,admin
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from backend.auth.routes import router as auth_router


app = FastAPI(title="C/Python Tutor API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )



app.include_router(auth_router)
app.include_router(meta.router)
app.include_router(chat.router)
app.include_router(admin.router)