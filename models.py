import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional

# Definición de modelos Pydantic para validar datos de pacientes
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


# Definición de modelo para registros médicos
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


# Carga y validación de pacientes
df_pacientes = pd.read_csv("pacientes.csv")
pacientes_validos = []

for _, row in df_pacientes.iterrows():
    try:
        paciente = Paciente(**row.to_dict())
        pacientes_validos.append(paciente)
    except ValidationError as e:
        print(f"Error en paciente ID {row['paciente_id']}: {e}")

# Carga y validación de registros médicos
df_registros = pd.read_csv("datos_salud_varios_pacientes.csv")
registros_validos = []

for _, row in df_registros.iterrows():
    try:
        registro = RegistroMedico(
            paciente_id=int(row["paciente_id"]),
            timestamp=pd.to_datetime(row["timestamp"]),
            ritmo_cardiaco=int(row["ritmo_cardiaco"]),
            spo2=float(row["spo2"]),
            temperatura=float(row["temperatura"]),
            frecuencia_respiratoria=int(row["frecuencia_respiratoria"]),
            presion_sistolica=int(row["presion_sistolica"]),
            presion_diastolica=int(row["presion_diastolica"]),
            actividad=row["actividad"],
            pasos=int(row["pasos"]),
            estado_animo=row["estado_animo"],
        )
        registros_validos.append(registro)
    except ValidationError as e:
        print(
            f"Error en registro paciente ID {row['paciente_id']} timestamp {row['timestamp']}: {e}"
        )

print(f"Pacientes válidos: {len(pacientes_validos)}")
print(f"Registros válidos: {len(registros_validos)}")
