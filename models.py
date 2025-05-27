import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional, Tuple
import random
import numpy as np
import os


# ----------------------------
# Modelos Pydantic
# ----------------------------

class Paciente(BaseModel):
    paciente_id: int
    nombre: str
    dni: str
    edad: int
    hospital: str
    ubicacion: str

    @validator("edad")
    def edad_valida(cls, v):
        if not (0 < v < 120):
            raise ValueError("Edad debe estar entre 1 y 119")
        return v


class RegistroMedico(BaseModel):
    paciente_id: int
    timestamp: datetime
    ritmo_cardiaco: int
    spo2: float
    temperatura: float
    frecuencia_respiratoria: int
    presion_sistolica: int
    presion_diastolica: int
    actividad: str
    pasos: int
    estado_animo: str

    @validator(
        "ritmo_cardiaco",
        "frecuencia_respiratoria",
        "presion_sistolica",
        "presion_diastolica",
        "pasos",
    )
    def valores_positivos(cls, v):
        if v < 0:
            raise ValueError("El valor debe ser positivo")
        return v

    @validator("spo2")
    def spo2_valido(cls, v):
        if not (0 <= v <= 100):
            raise ValueError("Spo2 debe estar entre 0 y 100")
        return v

    @validator("temperatura")
    def temperatura_valida(cls, v):
        if not (30 <= v <= 45):
            raise ValueError("Temperatura corporal fuera de rango")
        return v


# ----------------------------
# Funciones de validación
# ----------------------------

def validar_registro_dict(data: dict) -> Tuple[Optional[RegistroMedico], Optional[str]]:
    try:
        registro = RegistroMedico(
            paciente_id=int(data["paciente_id"]),
            timestamp=pd.to_datetime(data["timestamp"]),
            ritmo_cardiaco=int(data["ritmo_cardiaco"]),
            spo2=float(data["spo2"]),
            temperatura=float(data["temperatura"]),
            frecuencia_respiratoria=int(data["frecuencia_respiratoria"]),
            presion_sistolica=int(data["presion_sistolica"]),
            presion_diastolica=int(data["presion_diastolica"]),
            actividad=data["actividad"],
            pasos=int(data["pasos"]),
            estado_animo=data["estado_animo"],
        )
        return registro, None
    except ValidationError as e:
        return None, str(e)


# ----------------------------
# Generar CSV con errores para limpieza
# ----------------------------

def generar_registro_sucio(paciente_id: int) -> dict:
    actividades = ["reposo", "ligero", "moderado", "intensa"]
    estados = ["feliz", "neutro", "estresado", None]

    def maybe_wrong(val, prob=0.05, wrong_val=None):
        return wrong_val if random.random() < prob else val

    return {
        "paciente_id": paciente_id,
        "timestamp": datetime.now().isoformat(),
        "ritmo_cardiaco": maybe_wrong(random.randint(30, 200), 0.05, -20),
        "spo2": maybe_wrong(round(random.uniform(90, 100), 1), 0.05, 150),
        "temperatura": maybe_wrong(round(random.uniform(36.0, 38.5), 1), 0.05, 50),
        "frecuencia_respiratoria": maybe_wrong(random.randint(10, 25), 0.05, -5),
        "presion_sistolica": maybe_wrong(random.randint(90, 140), 0.05, 300),
        "presion_diastolica": maybe_wrong(random.randint(60, 90), 0.05, 10),
        "actividad": maybe_wrong(random.choice(actividades), 0.05, "desconocida"),
        "pasos": maybe_wrong(random.randint(0, 200), 0.05, -10),
        "estado_animo": random.choice(estados),
    }


# ----------------------------
# Generación de datos sucios
# ----------------------------

if __name__ == "__main__":
    # Crear carpeta si no existe
    os.makedirs("data", exist_ok=True)

    # Generar datos sucios
    registros_sucios = [generar_registro_sucio(random.randint(1, 10)) for _ in range(100)]
    
    # Introducir duplicados manualmente (últimos 5 duplican a los primeros 5)
    registros_sucios += registros_sucios[:5]

    df_sucios = pd.DataFrame(registros_sucios)
    df_sucios.to_csv("data/datos_salud.csv", index=False)

    print(" Archivo con datos generado: data/datos_salud.csv")