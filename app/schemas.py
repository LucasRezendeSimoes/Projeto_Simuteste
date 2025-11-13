from pydantic import BaseModel, EmailStr, field_validator, model_validator
from datetime import datetime, time
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(UserCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class LocationCreate(BaseModel):
    name: str
    capacity: int

class LocationRead(LocationCreate):
    id: int
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ResourceCreate(BaseModel):
    name: str
    resource_type: str

class ResourceRead(ResourceCreate):
    id: int
    availability: bool

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    user_id: int
    resource_id: int
    start_time: datetime
    duration_minutes: int
    notes: Optional[str] = None

    @field_validator("duration_minutes")
    @classmethod
    def duration_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("duration_minutes deve ser positivo")
        return v

    @model_validator(mode="after")
    def start_must_be_future(self):
        if self.start_time and self.start_time <= datetime.now():
            raise ValueError("start_time deve ser no futuro")
        return self

class AppointmentRead(BaseModel):
    id: int
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    location_id: int
    start_time: datetime
    end_time: datetime
    capacity: int

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time deve ser depois do start_time")
        return self

class EventRead(EventCreate):
    id: int
    description: Optional[str]

    class Config:
        from_attributes = True
