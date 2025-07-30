# pylint: disable=missing-class-docstring, too-few-public-methods, no-member
from sqlalchemy import Column, Integer, String, ForeignKey,Float, Date, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)

    patients = relationship("Patient", back_populates="study")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    study_id = Column(Integer, ForeignKey("studies.id"))

    study = relationship("Study", back_populates="patients")



class FollowUp(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    visit_no = Column(Integer)
    visit_date = Column(Date)
    dose_given = Column(Integer)
    side_effects = Column(Boolean)
    tumor_size = Column(Float)

    patient = relationship("Patient", backref="followups")
