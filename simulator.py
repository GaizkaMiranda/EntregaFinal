import time
import os
import random
import requests
from datetime import datetime

FASTAPI_HOST = os.getenv("FASTAPI_HOST", "fastapi")
FASTAPI_PORT = os.getenv("FASTAPI_PORT", "8000")
URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}/salud"

actividad_niveles = ["reposo", "ligero", "moderado", "intenso"]
estados_animo = ["neutro", "estresado", "feliz", "cansado"]


def generar_dato(paciente_id):
    return {
        "paciente_id": paciente_id,
        "timestamp": datetime.utcnow().isoformat(),
        "ritmo_cardiaco": random.randint(60, 100),
        "spo2": round(random.uniform(95, 100), 1),
        "temperatura": round(random.uniform(36.0, 37.5), 1),
        "frecuencia_respiratoria": random.randint(12, 20),
        "presion_sistolica": random.randint(100, 130),
        "presion_diastolica": random.randint(60, 85),
        "actividad": random.choice(actividad_niveles),
        "pasos": random.randint(0, 200),
        "estado_animo": random.choice(estados_animo),
    }


if __name__ == "__main__":
    pacientes = list(range(1, 11))
    intervalo = int(os.getenv("SIM_INTERVAL", "10"))  # segundos
    while True:
        for pid in pacientes:
            dato = generar_dato(pid)
            try:
                resp = requests.post(URL, json=dato)
                print(f"Enviado paciente {pid}:", resp.status_code)
            except Exception as e:
                print("Error al enviar:", e)
        time.sleep(intervalo)
