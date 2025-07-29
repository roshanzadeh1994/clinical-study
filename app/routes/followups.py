from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import csv
import io
from io import TextIOWrapper
from ..database import SessionLocal
from .. import models, schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(prefix="/followups", tags=["FollowUps"])


@router.post("/upload_csv")
async def upload_followups_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    content = await file.read()
    decoded_stream = io.StringIO(content.decode("utf-8"), newline='')  # ← اصلاح اصلی اینجاست
    reader = csv.DictReader(decoded_stream)


    records_created = 0
    for row in reader:
        try:
            followup = models.FollowUp(
                patient_id=int(row["patient_id"]),
                visit_no=int(row["visit_no"]),
                visit_date=row["visit_date"],
                dose_given=int(row["dose_given"]),
                side_effects=row["side_effects"].lower() == "true",
                tumor_size=float(row["tumor_size"]),
            )
            db.add(followup)
            records_created += 1
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error in row: {row} | {e}")

    db.commit()
    return {"message": f"{records_created} follow-up records successfully imported."}
