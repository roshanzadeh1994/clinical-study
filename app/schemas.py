from pydantic import BaseModel

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
