import csv
import time
import os
from models import validar_registro_dict

DATA_DIR = "/data"
INPUT_FILE = os.path.join(DATA_DIR, "datos_salud.csv")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_registros.csv")
ERROR_FILE = os.path.join(DATA_DIR, "errores_registros.csv")
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
INTERVAL = int(os.getenv("PROCESS_INTERVAL", "15"))  # en segundos

# Asegurarnos de que los CSV destino existen con su cabecera
def ensure_file(path, fieldnames):
    if not os.path.isfile(path):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()


ensure_file(PROCESSED_FILE, FIELDNAMES)
ensure_file(ERROR_FILE, FIELDNAMES + ["error"])

while True:
    # Solo si existe y tiene más que la cabecera
    if os.path.isfile(INPUT_FILE) and os.path.getsize(INPUT_FILE) > 0:
        with open(INPUT_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Si solo está la cabecera, no hacer nada
        if rows:
            validos = []
            errores = []

            for row in rows:
                registro, err = validar_registro_dict(row)
                if registro:
                    validos.append(registro.dict())
                else:
                    row["error"] = err
                    errores.append(row)

            # Escribir válidos
            with open(PROCESSED_FILE, "a", newline="") as f_ok:
                writer = csv.DictWriter(f_ok, fieldnames=FIELDNAMES)
                for v in validos:
                    writer.writerow(v)

            # Escribir errores
            with open(ERROR_FILE, "a", newline="") as f_er:
                writer = csv.DictWriter(f_er, fieldnames=FIELDNAMES + ["error"])
                for e in errores:
                    writer.writerow(e)

            # **Reescribir el CSV de entrada solo con la cabecera**
            with open(INPUT_FILE, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()

            print(
                f"Procesadas {len(rows)} líneas: {len(validos)} válidas, {len(errores)} errores."
            )

    time.sleep(INTERVAL)
