from pydantic import BaseModel
from datetime import date

class StudyCreate(BaseModel):
    title: str
    description: str

class StudyOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True

class PatientCreate(BaseModel):
    name: str
    age: int
    study_id: int

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    study_id: int

    class Config:
        orm_mode = True



class FollowUpBase(BaseModel):
    visit_no: int
    visit_date: date
    dose_given: int
    side_effects: bool
    tumor_size: float

class FollowUpCreate(FollowUpBase):
    patient_id: int

class FollowUpOut(FollowUpBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True
