import csv
import time
import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from models import validar_registro_dict

# --- Configuración InfluxDB vía variables de entorno ---
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "deusto2024-secret-token")
INFLUX_ORG = os.getenv("INFLUX_ORG", "deusto-org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "deusto-bucket")

# --- Rutas y nombres de archivo ---
DATA_DIR = "/data"
INPUT_FILE = os.path.join(DATA_DIR, "datos_salud.csv")
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
INTERVAL = int(os.getenv("PROCESS_INTERVAL", "10"))  # segundos

# --- Inicializar CSV de errores con cabecera si no existe ---
if not os.path.isfile(ERROR_FILE):
    with open(ERROR_FILE, "w", newline="") as f_err:
        writer = csv.DictWriter(f_err, fieldnames=FIELDNAMES + ["error"])
        writer.writeheader()

# --- Conexión a InfluxDB ---
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_precision=WritePrecision.NS)

while True:
    # Solo si el CSV de entrada existe y tiene más que la cabecera
    if os.path.isfile(INPUT_FILE) and os.path.getsize(INPUT_FILE) > 0:
        with open(INPUT_FILE, "r", newline="") as f_in:
            reader = csv.DictReader(f_in)
            rows = list(reader)

        if rows:
            errores = []

            for row in rows:
                registro, err = validar_registro_dict(row)
                if registro:
                    # Crear punto InfluxDB
                    dt = registro.timestamp
                    timestamp = int(dt.timestamp() * 1e9)
                    point = (
                        Point("salud")
                        .tag("paciente_id", str(registro.paciente_id))
                        .tag("actividad", registro.actividad)
                        .tag("estado_animo", registro.estado_animo)
                        .field("ritmo_cardiaco", registro.ritmo_cardiaco)
                        .field("spo2", registro.spo2)
                        .field("temperatura", registro.temperatura)
                        .field(
                            "frecuencia_respiratoria", registro.frecuencia_respiratoria
                        )
                        .field("presion_sistolica", registro.presion_sistolica)
                        .field("presion_diastolica", registro.presion_diastolica)
                        .field("pasos", registro.pasos)
                        .time(timestamp, WritePrecision.NS)
                    )
                    # Envío a Influx
                    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
                else:
                    # Registrar error
                    row["error"] = err
                    errores.append(row)

            # Flush para garantizar envío
            write_api.flush()

            # Escribir errores acumulados
            if errores:
                with open(ERROR_FILE, "a", newline="") as f_err:
                    writer = csv.DictWriter(f_err, fieldnames=FIELDNAMES + ["error"])
                    for e in errores:
                        writer.writerow(e)

            # **Reescribir solo la cabecera en el CSV de entrada**
            with open(INPUT_FILE, "w", newline="") as f_trunc:
                writer = csv.DictWriter(f_trunc, fieldnames=FIELDNAMES)
                writer.writeheader()

            print(
                f"Procesadas {len(rows)} líneas: "
                f"{len(rows)-len(errores)} subidas a Influx, {len(errores)} errores."
            )

    time.sleep(INTERVAL)
