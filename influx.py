from influxdb_client import InfluxDBClient, Point, WritePrecision
import csv
from datetime import datetime

token = "deusto2024-secret-token"
org = "deusto-org"
bucket = "deusto-bucket"
url = "http://localhost:8088" 

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_precision=WritePrecision.NS)


with open('datos_salud_varios_pacientes.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dt = datetime.fromisoformat(row['timestamp'])
        timestamp = int(dt.timestamp() * 1e9)
        
        point = (
            Point("salud")
            .tag("paciente_id", row["paciente_id"])
            .tag("actividad", row["actividad"])
            .tag("estado_animo", row["estado_animo"])
            .field("ritmo_cardiaco", float(row["ritmo_cardiaco"]))
            .field("spo2", float(row["spo2"]))
            .field("temperatura", float(row["temperatura"]))
            .field("frecuencia_respiratoria", int(row["frecuencia_respiratoria"]))
            .field("presion_sistolica", int(row["presion_sistolica"]))
            .field("presion_diastolica", int(row["presion_diastolica"]))
            .field("pasos", int(row["pasos"]))
            .time(timestamp, WritePrecision.NS)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        
write_api.__del__()
client.__del__()
print("Datos importados correctamente a InfluxDB.")
