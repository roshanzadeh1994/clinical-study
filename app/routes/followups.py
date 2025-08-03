from io import StringIO
import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]

from app.db.models import FollowUp, Patient
from app.routes.studies import get_db

router = APIRouter(prefix="/followups", tags=["Followups"])

@router.post("/upload_csv")
async def upload_followups_csv(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    df = pd.read_csv(StringIO(decoded))

    # ستون‌های مورد نیاز
    required_columns = {
        "patient_id", "visit_no", "visit_date",
        "dose_given", "side_effects", "tumor_size"
    }

    if not required_columns.issubset(df.columns):
        return {"error": f"Missing columns. Required: {required_columns}"}

    # تبدیل به داده‌های مناسب
    try:
        df["visit_date"] = pd.to_datetime(df["visit_date"]).dt.date
        df["side_effects"] = df["side_effects"].astype(bool)
    except Exception as e:
        return {"error": f"Invalid data types in CSV: {str(e)}"}

    # استخراج تمام patient_id‌های معتبر از جدول patient
    valid_ids = {p.id for p in db.query(Patient.id).all()}
    invalid_ids = set(df["patient_id"]) - valid_ids

    if invalid_ids:
        return {
            "error": f"The following patient_ids do not exist: {sorted(invalid_ids)}"
        }

    # تبدیل به ORM
    followups = [
        FollowUp(
            patient_id=int(row["patient_id"]),
            visit_no=int(row["visit_no"]),
            visit_date=row["visit_date"],
            dose_given=int(row["dose_given"]),
            side_effects=bool(row["side_effects"]),
            tumor_size=float(row["tumor_size"]),
        )
        for _, row in df.iterrows()
    ]

    db.add_all(followups)
    db.commit()

    return {"message": f"{len(followups)} followups successfully inserted."}
