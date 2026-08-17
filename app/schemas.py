from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator


class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str


class PatientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str

    model_config = {"from_attributes": True}


class DoctorCreate(BaseModel):
    name: str
    specialization: str


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str

    model_config = {"from_attributes": True}


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.appointment_end <= self.appointment_start:
            raise ValueError("appointment_end must be after appointment_start")

        return self


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime

    model_config = {"from_attributes": True}
