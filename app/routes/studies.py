from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import models
from .. import schemas

from ..db.database import SessionLocal
 
router = APIRouter(prefix="/studies", tags=["Studies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/studies/", response_model=schemas.StudyOut)
def create_study(study: schemas.StudyCreate, db: Session = Depends(get_db)):
    new_study = models.Study(**study.dict())
    db.add(new_study)
    db.commit()
    db.refresh(new_study)
    return new_study

@router.get("/studies/", response_model=list[schemas.StudyOut])
def get_studies(db: Session = Depends(get_db)):
    return db.query(models.Study).all()