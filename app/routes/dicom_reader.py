from fastapi import APIRouter, UploadFile, File
import pydicom
import shutil
import os
from PIL import Image
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response, JSONResponse
from io import BytesIO

router = APIRouter(tags=["Dicom"])




router = APIRouter(tags=["Dicom"])

UPLOAD_DIR = "./images-dicom"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def dicom_to_png_bytes(dicom_path):
    ds = pydicom.dcmread(dicom_path)
    
    # گرفتن تصویر
    pixel_array = ds.pixel_array
    pixel_array = np.squeeze(pixel_array)  # حذف ابعاد اضافی (1,1,X) → (X)

    # بررسی نهایی اینکه دوبعدیه
    if pixel_array.ndim != 2:
        raise ValueError(f"Unsupported pixel array shape: {pixel_array.shape}")

    # نرمال‌سازی
    if np.ptp(pixel_array) > 0:
        image_2d = (pixel_array - np.min(pixel_array)) / np.ptp(pixel_array) * 255.0
    else:
        image_2d = np.zeros_like(pixel_array)

    image_2d = image_2d.astype(np.uint8)

    # ساخت تصویر و تبدیل به bytes
    img = Image.fromarray(image_2d)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf



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





@router.post("/dicom/upload-preview")
async def upload_and_preview(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        img_bytes = dicom_to_png_bytes(file_path)
        return Response(content=img_bytes.read(), media_type="image/png")
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
