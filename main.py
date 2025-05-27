from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import csv
import os

app = FastAPI()

DATA_DIR = "/data"
CSV_FILE = os.path.join(DATA_DIR, "datos_salud_limpios.csv")
FIELDNAMES = [
    "paciente_id",
    "timestamp",
    "ritmo_cardiaco",
    "spo2",
    "temperatura",
    "frecuencia_respiratoria",
    "presion_sistolica",
    "presion_diastolica",
    "actividad",
    "pasos",
    "estado_animo",
]

# Crear carpeta y CSV con cabecera si no existe
def init_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


class RegistroMedico(BaseModel):
    paciente_id: int
    timestamp: datetime
    ritmo_cardiaco: int
    spo2: float = Field(..., ge=0, le=100)
    temperatura: float = Field(..., ge=30, le=45)
    frecuencia_respiratoria: int
    presion_sistolica: int
    presion_diastolica: int
    actividad: str
    pasos: int
    estado_animo: str


@app.on_event("startup")
def startup_event():
    init_csv()


@app.post("/salud")
def post_salud(registro: RegistroMedico):
    try:
        row = registro.dict()
        # Convertir timestamp a ISO
        row["timestamp"] = row["timestamp"].isoformat()
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writerow(row)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
