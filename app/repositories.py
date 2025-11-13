from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from . import models
from sqlalchemy.orm import Session

# Interface (abstração) — Repository Pattern
class UserRepository(ABC):
    @abstractmethod
    def create(self, db: Session, user: models.User) -> models.User: ...
    @abstractmethod
    def get(self, db: Session, user_id: int) -> Optional[models.User]: ...
    @abstractmethod
    def list(self, db: Session, skip: int=0, limit: int=100) -> List[models.User]: ...
    @abstractmethod
    def update(self, db: Session, user: models.User) -> models.User: ...
    @abstractmethod
    def delete(self, db: Session, user_id: int) -> None: ...

# Implementação concreta para SQLite (SQLAlchemy)
class SqlAlchemyUserRepository(UserRepository):
    def create(self, db: Session, user: models.User) -> models.User:
        db.add(user); db.commit(); db.refresh(user)
        return user

    def get(self, db: Session, user_id: int) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.id == user_id).first()

    def list(self, db: Session, skip: int=0, limit: int=100):
        return db.query(models.User).offset(skip).limit(limit).all()

    def update(self, db: Session, user: models.User) -> models.User:
        db.merge(user)
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> None:
        u = db.query(models.User).filter(models.User.id == user_id).first()
        if u:
            db.delete(u); db.commit()

# Repositórios para Appointment, Resource, Location, Event seguem padrão semelhante:
class AppointmentRepository(ABC):
    @abstractmethod
    def create(self, db: Session, app: models.Appointment) -> models.Appointment: ...
    @abstractmethod
    def get(self, db: Session, id: int) -> Optional[models.Appointment]: ...
    @abstractmethod
    def list_by_filter(self, db: Session, user_id: Optional[int]=None,
                       start: Optional[datetime]=None, end: Optional[datetime]=None,
                       order_by: str = "start_time") -> List[models.Appointment]: ...
    @abstractmethod
    def update(self, db: Session, app: models.Appointment) -> models.Appointment: ...
    @abstractmethod
    def delete(self, db: Session, id: int) -> None: ...

class SqlAlchemyAppointmentRepository(AppointmentRepository):
    def create(self, db: Session, app: models.Appointment) -> models.Appointment:
        db.add(app); db.commit(); db.refresh(app); return app

    def get(self, db: Session, id: int):
        return db.query(models.Appointment).filter(models.Appointment.id == id).first()

    def list_by_filter(self, db: Session, user_id=None, start=None, end=None, order_by="start_time"):
        q = db.query(models.Appointment)
        if user_id:
            q = q.filter(models.Appointment.user_id == user_id)
        if start:
            q = q.filter(models.Appointment.start_time >= start)
        if end:
            q = q.filter(models.Appointment.end_time <= end)
        if order_by == "start_time":
            q = q.order_by(models.Appointment.start_time)
        return q.all()

    def update(self, db: Session, app: models.Appointment):
        db.merge(app); db.commit(); db.refresh(app); return app

    def delete(self, db: Session, id: int):
        a = db.query(models.Appointment).filter(models.Appointment.id == id).first()
        if a:
            db.delete(a); db.commit()

# Você pode implementar ResourceRepository, LocationRepository, EventRepository do mesmo jeito.
# Para manter o exemplo enxuto, só incluí os dois acima — no projeto real copie o padrão para todas as entidades.
