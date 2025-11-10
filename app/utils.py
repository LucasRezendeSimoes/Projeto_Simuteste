import os
from app.config import CONFIG
from typing import List
from datetime import datetime
import csv
from app.models import Appointment

def ensure_export_dir():
    d = CONFIG["export"]["csv_dir"]
    os.makedirs(d, exist_ok=True)
    return d

def export_appointments_to_csv(appointments: List[Appointment]) -> str:
    """Exporta lista de appointments para CSV e retorna path."""
    d = ensure_export_dir()
    filename = f"appointments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = os.path.join(d, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "user_id", "resource_id", "start_time", "end_time", "status", "notes"])
        for a in appointments:
            w.writerow([a.id, a.user_id, a.resource_id, a.start_time.isoformat(), a.end_time.isoformat(), a.status, a.notes or ""])
    return path
