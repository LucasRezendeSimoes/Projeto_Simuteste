from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class User(Base):
    """Usuário que agenda/consulta."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    # relacionamento
    appointments = relationship("Appointment", back_populates="user")

class Location(Base):
    """Local onde um evento/consulta pode ocorrer."""
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, default=1)
    description = Column(Text, nullable=True)
    events = relationship("Event", back_populates="location")

class Resource(Base):
    """Recurso (sala, equipamento, médico etc.)"""
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    availability = Column(Boolean, default=True)
    appointments = relationship("Appointment", back_populates="resource")

class Appointment(Base):
    """Reserva/consulta agendada."""
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")  # scheduled / done / cancelled
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="appointments")
    resource = relationship("Resource", back_populates="appointments")

class Event(Base):
    """Eventos que podem envolver várias pessoas (ex.: workshop)."""
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    capacity = Column(Integer, default=10)
    description = Column(Text, nullable=True)

    location = relationship("Location", back_populates="events")
