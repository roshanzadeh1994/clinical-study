from fastapi import APIRouter, UploadFile, File
import pydicom
import shutil
import os
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Dicom"])

UPLOAD_DIR = "./images-dicom/001848_001.dcm"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/dicom/upload")
async def upload_dicom(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ds = pydicom.dcmread(file_location)

        metadata = {
            "PatientName": str(ds.get("PatientName", "N/A")),
            "Modality": str(ds.get("Modality", "N/A")),
            "StudyDate": str(ds.get("StudyDate", "N/A")),
            "FileSavedAs": file.filename
        }

        return JSONResponse(content=metadata)
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
