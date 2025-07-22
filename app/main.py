from fastapi import FastAPI
from app.routes import studies, patients  # نسبی نیست چون با app.main اجرا می‌کنی
from fastapi.responses import JSONResponse

app = FastAPI()

# Routers
app.include_router(studies.router)
app.include_router(patients.router)

import logging

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
