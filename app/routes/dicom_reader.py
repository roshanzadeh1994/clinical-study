from fastapi import APIRouter, UploadFile, File
import pydicom
import shutil
import os
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
import numpy as np

router = APIRouter(tags=["Dicom"])




def dicom_to_png(dicom_path, output_path):
    ds = pydicom.dcmread(dicom_path)

    # بررسی وجود داده تصویری
    if not hasattr(ds, 'pixel_array'):
        raise ValueError("No pixel data found in DICOM file.")

    pixel_array = ds.pixel_array.astype(float)

    # نرمال‌سازی به 0-255 و تبدیل به تصویر خاکستری
    normalized = ((pixel_array - pixel_array.min()) / (pixel_array.ptp()) * 255.0).astype(np.uint8)
    image = Image.fromarray(normalized).convert("L")
    image.save(output_path)

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



@router.get("/dicom/preview/{filename}")
async def preview_dicom(filename: str):
    dicom_path = f"{UPLOAD_DIR}/{filename}"
    png_path = f"{UPLOAD_DIR}/{filename}.png"

    try:
        dicom_to_png(dicom_path, png_path)
        return FileResponse(png_path, media_type="image/png")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
