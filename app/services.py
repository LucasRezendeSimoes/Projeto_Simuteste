from datetime import timedelta, datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories import SqlAlchemyAppointmentRepository, SqlAlchemyUserRepository
from app import models
from app.exceptions import NotFoundException, BusinessRuleException
from app.config import CONFIG

class AppointmentService:
    """
    Camada de lógica de negócio para Agendamentos.
    - Aplica regras: ausência de conflito de horários, horário de trabalho, limite por usuário.
    - Calcula end_time a partir do duration.
    """
    def __init__(self, appointment_repo: SqlAlchemyAppointmentRepository, user_repo: SqlAlchemyUserRepository):
        self.app_repo = appointment_repo
        self.user_repo = user_repo
        cfg = CONFIG["app"]
        wh = CONFIG["app"]["working_hours"]
        start_h, end_h = wh["start"], wh["end"]
        self.working_start = time.fromisoformat(start_h)
        self.working_end = time.fromisoformat(end_h)

    def create_appointment(self, db: Session, user_id: int, resource_id: int,
                           start_time: datetime, duration_minutes: int, notes: Optional[str]=None) -> models.Appointment:
        """
        Regras complexas (exemplos):
        1) Validação de múltiplas condições:
           - horário dentro do expediente (working_hours)
           - usuário ativo
           - duração positiva (validado no schema)
        2) Cálculo:
           - calcula end_time = start_time + duration
           - calcula total horas diárias do usuário ao criar
        3) Interação entre entidades:
           - checa se recurso já está ocupado (overlap)
           - checa número máximo de agendamentos do usuário no mesmo dia (ex: 3)
        """
        user = self.user_repo.get(db, user_id)
        if not user:
            raise NotFoundException("Usuário não encontrado")
        if not user.is_active:
            raise BusinessRuleException("Usuário inativo")

        end_time = start_time + timedelta(minutes=duration_minutes)

        # Regra: horário dentro do expediente
        if not (self.working_start <= start_time.time() < self.working_end and self.working_start < end_time.time() <= self.working_end):
            raise BusinessRuleException(f"Agendamento fora do expediente ({self.working_start} - {self.working_end})")

        # Regra: limite de agendamentos por usuário por dia
        day_start = datetime.combine(start_time.date(), time.min)
        day_end = datetime.combine(start_time.date(), time.max)
        user_apps = self.app_repo.list_by_filter(db, user_id=user_id, start=day_start, end=day_end)
        if len(user_apps) >= 3:
            raise BusinessRuleException("Usuário atingiu limite diário de 3 agendamentos")

        # Regra: evitar overlap no mesmo recurso
        all_resource_apps = db.query(models.Appointment).filter(models.Appointment.resource_id == resource_id).all()
        for a in all_resource_apps:
            # overlap check
            if not (end_time <= a.start_time or start_time >= a.end_time):
                raise BusinessRuleException("Conflito com outro agendamento no recurso (sobreposição)")

        # Se passou, cria
        appointment = models.Appointment(
            user_id=user_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )
        return self.app_repo.create(db, appointment)

    def export_appointments_csv(self, db: Session, file_path: str):
        """
        Exporta todos agendamentos para CSV (manipulação de arquivo).
        """
        import csv
        apps = db.query(models.Appointment).all()
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "user_id", "resource_id", "start_time", "end_time", "status", "notes"])
            for a in apps:
                writer.writerow([a.id, a.user_id, a.resource_id, a.start_time.isoformat(), a.end_time.isoformat(), a.status, a.notes or ""])

class UserService:
    """Serviços para usuários (ex.: cálculo de horas reservadas)"""
    def __init__(self, user_repo: SqlAlchemyUserRepository, appointment_repo: SqlAlchemyAppointmentRepository):
        self.user_repo = user_repo
        self.app_repo = appointment_repo

    def total_reserved_minutes(self, db: Session, user_id: int) -> int:
        """Calcula total de minutos agendados do usuário no futuro."""
        apps = db.query(models.Appointment).filter(models.Appointment.user_id == user_id, models.Appointment.end_time > datetime.now()).all()
        total = sum(int((a.end_time - a.start_time).total_seconds() / 60) for a in apps)
        return total
