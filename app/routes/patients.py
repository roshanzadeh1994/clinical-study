from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.studies import get_db
from ..db import models
from .. import schemas

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/patients/", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.get("/patients/", response_model=list[schemas.PatientOut])
def get_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()


@router.get("/studies/{study_id}/patients", response_model=list[schemas.PatientOut])
def get_patients_for_study(study_id: int, db: Session = Depends(get_db)):
    study = db.query(models.Study).filter(models.Study.id == study_id).first()
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")
    return study.patients
