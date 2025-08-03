from fastapi import FastAPI
from app.routes import studies, patients,followups,analysis ,dicom_reader # نسبی نیست چون با app.main اجرا می‌کنی
from fastapi.responses import JSONResponse
from app.db.database import Base, engine
import logging

app = FastAPI()

Base.metadata.create_all(bind=engine)
# Routers
app.include_router(studies.router)
app.include_router(patients.router)
app.include_router(followups.router)
app.include_router(analysis.router)
app.include_router(dicom_reader.router)  





@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
