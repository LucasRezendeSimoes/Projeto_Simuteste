import pytest
from datetime import datetime, timedelta
from app.services import AppointmentService
from app.repositories import SqlAlchemyAppointmentRepository, SqlAlchemyUserRepository
from app.exceptions import BusinessRuleException, NotFoundException
from types import SimpleNamespace

class FakeUserRepo(SqlAlchemyUserRepository):
    def __init__(self):
        self.storage = {}

    def get(self, db, user_id):
        return self.storage.get(user_id)

class FakeAppointmentRepo(SqlAlchemyAppointmentRepository):
    def __init__(self):
        self.storage = []

    def list_by_filter(self, db, user_id=None, start=None, end=None, order_by="start_time"):
        return [a for a in self.storage if a.user_id == user_id] if user_id else self.storage

    def create(self, db, app):
        app.id = len(self.storage) + 1
        self.storage.append(app)
        return app

def test_create_appointment_outside_working_hours():
    fake_user_repo = FakeUserRepo()
    fake_appt_repo = FakeAppointmentRepo()
    service = AppointmentService(fake_appt_repo, fake_user_repo)
    # usuário não existe -> NotFound
    with pytest.raises(NotFoundException):
        service.create_appointment(None, 1, 1, datetime.now() + timedelta(days=1), 30)
