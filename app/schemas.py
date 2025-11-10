from pydantic import BaseModel, EmailStr, validator, root_validator
from datetime import datetime, time
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(UserCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class LocationCreate(BaseModel):
    name: str
    capacity: int

class LocationRead(LocationCreate):
    id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ResourceCreate(BaseModel):
    name: str
    resource_type: str

class ResourceRead(ResourceCreate):
    id: int
    availability: bool

    class Config:
        orm_mode = True

class AppointmentCreate(BaseModel):
    user_id: int
    resource_id: int
    start_time: datetime
    duration_minutes: int
    notes: Optional[str] = None

    @validator("duration_minutes")
    def duration_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("duration_minutes deve ser positivo")
        return v

    @root_validator
    def start_must_be_future(cls, values):
        start = values.get("start_time")
        if start and start <= datetime.now():
            raise ValueError("start_time deve ser no futuro")
        return values

class AppointmentRead(BaseModel):
    id: int
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: str
    notes: Optional[str]

    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    title: str
    location_id: int
    start_time: datetime
    end_time: datetime
    capacity: int

    @root_validator
    def end_after_start(cls, values):
        if values.get("end_time") <= values.get("start_time"):
            raise ValueError("end_time deve ser depois do start_time")
        return values

class EventRead(EventCreate):
    id: int
    description: Optional[str]

    class Config:
        orm_mode = True
