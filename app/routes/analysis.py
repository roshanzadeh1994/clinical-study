from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.routes.studies import get_db
from app.db.models import FollowUp
import csv
import io

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get(
    "/analysis/followups_csv"
)
def export_followups_csv(db: Session = Depends(get_db)):
    followups = db.query(FollowUp).all()

    # آماده‌سازی فایل CSV در حافظه
    output = io.StringIO()
    writer = csv.writer(output)

    # نوشتن header
    writer.writerow(
        [
            "patient_id",
            "visit_no",
            "visit_date",
            "dose_given",
            "side_effects",
            "tumor_size",
        ]
    )

    # نوشتن داده‌ها
    for f in followups:
        writer.writerow(
            [
                f.patient_id,
                f.visit_no,
                f.visit_date,
                f.dose_given,
                f.side_effects,
                f.tumor_size,
            ]
        )

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=followups.csv"},
    )
