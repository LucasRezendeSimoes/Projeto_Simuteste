from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .db import get_db
from . import schemas, models
from .repositories import SqlAlchemyUserRepository, SqlAlchemyAppointmentRepository
from .services import AppointmentService, UserService
from .exceptions import AppException, NotFoundException, BusinessRuleException
from .config import CONFIG
from typing import List, Optional
from datetime import datetime, date, timedelta
from .utils import export_appointments_to_csv
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# DI: Repositories instanciadas (poderiam vir de um contêiner)
user_repo = SqlAlchemyUserRepository()
app_repo = SqlAlchemyAppointmentRepository()

# Services
appointment_service = AppointmentService(app_repo, user_repo)
user_service = UserService(user_repo, app_repo)

@router.post("/users", response_model=schemas.UserRead)
def create_user(u: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create user (CRUD 1)."""
    user = models.User(name=u.name, email=u.email)
    try:
        created = user_repo.create(db, user)
        logger.info("User created %s", created.id)
        return created
    except Exception as e:
        logger.exception("Failed to create user")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    u = user_repo.get(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repo.delete(db, user_id)
    return {}

# --- Appointments CRUD ---
@router.post("/appointments", response_model=schemas.AppointmentRead)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        appt = appointment_service.create_appointment(db, payload.user_id, payload.resource_id, payload.start_time, payload.duration_minutes, payload.notes)
        return appt
    except BusinessRuleException as e:
        logger.warning("Business rule failed: %s", e)
        raise HTTPException(status_code=422, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error creating appointment")
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get("/appointments", response_model=List[schemas.AppointmentRead])
def list_appointments(user_id: Optional[int] = None, start: Optional[datetime] = None, end: Optional[datetime] = None, order_by: str = "start_time", db: Session = Depends(get_db)):
    """Consulta com filtros e ordenação (requisito)."""
    return app_repo.list_by_filter(db, user_id=user_id, start=start, end=end, order_by=order_by)

@router.get("/appointments/export")
def export_appointments(db: Session = Depends(get_db)):
    """Exporta appointments para CSV (manipulação de arquivo)."""
    apps = db.query(models.Appointment).all()
    path = export_appointments_to_csv(apps)
    return {"path": path}

@router.get("/users/{user_id}/reserved_minutes")
def get_reserved_minutes(user_id: int, db: Session = Depends(get_db)):
    tot = user_service.total_reserved_minutes(db, user_id)
    return {"user_id": user_id, "reserved_minutes": tot}
