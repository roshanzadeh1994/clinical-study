from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.routes.studies import get_db
from app.db.models import FollowUp
import pandas as pd
import io

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/analysis/followups_csv")
def export_followups_csv(db: Session = Depends(get_db)):
    followups = db.query(FollowUp).all()

    # ساخت DataFrame از داده‌های ORM
    df = pd.DataFrame([{
        "patient_id": f.patient_id,
        "visit_no": f.visit_no,
        "visit_date": f.visit_date,
        "dose_given": f.dose_given,
        "side_effects": f.side_effects,
        "tumor_size": f.tumor_size,
    } for f in followups])

    # ذخیره در CSV در حافظه
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=followups.csv"},
    )
