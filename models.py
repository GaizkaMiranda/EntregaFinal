import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional, Tuple


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
    """
    Intenta validar un registro a partir de un dict.
    Devuelve una tupla (RegistroMedico, None) si es válido,
    o (None, mensaje_error) si no lo es.
    """
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
# Carga y validación en bloque
# (opcional: solo si necesitas ejecutar standalone)
# ----------------------------

if __name__ == "__main__":
    # Validar pacientes.csv
    df_pacientes = pd.read_csv("pacientes.csv")
    pacientes_validos = []
    for _, row in df_pacientes.iterrows():
        try:
            p = Paciente(**row.to_dict())
            pacientes_validos.append(p)
        except ValidationError as e:
            print(f"Error en paciente ID {row['paciente_id']}: {e}")

    print(f"Pacientes válidos: {len(pacientes_validos)}")

    # Validar datos_salud_v.csv
    df_registros = pd.read_csv("datos_salud_v.csv")
    registros_validos = []
    for _, row in df_registros.iterrows():
        reg, err = validar_registro_dict(row.to_dict())
        if reg:
            registros_validos.append(reg)
        else:
            print(f"Error en registro {row.to_dict()}: {err}")

    print(f"Registros válidos: {len(registros_validos)}")
