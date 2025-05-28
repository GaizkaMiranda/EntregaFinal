 # ENTREGA FINAL

Este proyecto es el resultado de una colaboración entre Gaizka Miranda, Ekaitz García y Eneko Fuente. El objetivo principal es demostrar la integración y funcionamiento de diversas tecnologías como FASTAPI, INFLUXDB y GRAFANA dentro de un entorno contenerizado con DOCKER.

---

## COLABORADORES

- **GAIZKA MIRANDA** – Estudiante en Deusto  
- **EKAITZ GARCÍA** – Estudiante en Deusto  
- **ENEKO FUENTE** – Estudiante en Deusto  

---

## INSTALACIÓN

Sigue estos pasos para clonar y configurar el proyecto localmente:

```bash
git clone https://github.com/GaizkaMiranda/EntregaFinal.git
cd EntregaFinal
# INSTALAR DEPENDENCIAS
pip install -r requirements.txt
```

---

## CÓMO EJECUTAR

### 1. EJECUTAR DOCKER COMPOSE

Desde la carpeta raíz del proyecto (donde se encuentra `docker-compose.yml`), ejecuta:

```bash
sudo docker-compose up -d
```

### 2. VERIFICAR EL ESTADO DE LOS CONTENEDORES

```bash
sudo docker-compose ps
```

### 3. ACCEDER A LOS SERVICIOS

- **FASTAPI**: [http://localhost:8000](http://localhost:8000)  
- **GRAFANA**: [http://localhost:3000](http://localhost:3000)  
- **INFLUXDB**: [http://localhost:8086](http://localhost:8086)

### 4. DETENER LOS CONTENEDORES

```bash
sudo docker-compose down
```

### 5. Ejecutar n8n
- Crear una cuenta en n8n cloud
- Importar el flujo “Automatizacion_was.json”
- Establecer las conexiones pertinentes (whatsapp y openAI)
- Ejecutar ngrok http --url=usable-fox-flying.ngrok-free.app 8086 en la carpeta raíz de ngrok (el comando puede cambiar pero es el que ngrok te da para crear un tunel en un dominio estatico)
- Pegar en n8n el url que se obtenga.
- Credenciales n8n:
  - url: https://deusto.app.n8n.cloud/
  - email: ekaitzgarci@gmail.com
  - password: Deusto2025


---

## CONFIGURACIÓN

### INFLUXDB

Después de iniciar los contenedores con `docker-compose up`, accede con:

- **USUARIO**: `Deusto`  
- **CONTRASEÑA**: `deusto2025`

### GRAFANA

#### INTEGRACIÓN DE INFLUXDB COMO DATASOURCE:

- **LENGUAJE DE CONSULTA**: FLUX  
- **URL**: `http://influxdb:8086`
- **CREDENCIALES DE ADMIN**:
  - USUARIO: `admin` o 
  - CONTRASEÑA: `admin`
- **CREDENCIALES DE INFLUXDB**:
  - ORGANIZACIÓN: `deusto-org`
  - TOKEN: `deusto2025-secret-token`
  - BUCKET: `deusto-bucket`

Después, ve al menú de **DASHBOARDS** e importa el dashboard ubicado en la carpeta del proyecto final.

---

## FASTAPI

### ENDPOINT PRINCIPAL

- `POST /salud`: Recibe datos médicos de un paciente y los guarda en un archivo CSV persistente dentro del contenedor.

### ESTRUCTURA DEL CÓDIGO

#### `MODELS.PY`

Define dos modelos con **PYDANTIC**:

- **PACIENTE**: Incluye campos como ID, nombre, DNI, edad, hospital y ubicación. Valida que la edad esté entre 1 y 119 años.
- **REGISTROMEDICO**: Incluye métricas médicas como ritmo cardíaco, SPO2, temperatura, presión arterial, pasos, etc. Incluye múltiples validadores para garantizar la validez de los datos.

Además, se incluyen funciones para:

- Validar un único registro desde un `dict` (`validar_registro_dict`)
- Validar archivos CSV completos (cuando se ejecuta standalone)

#### `MAIN.PY`

- Configura la app con **FASTAPI**.
- Crea el archivo `datos_salud.csv` si no existe al iniciar la app.
- Define el endpoint `/salud` que:
  - Recibe un objeto `RegistroMedico`.
  - Convierte el timestamp a ISO.
  - Guarda los datos en un archivo CSV con cabecera definida.

---

## OTROS ARCHIVOS

- **`DOCKER-COMPOSE.YML`**: Define los servicios (FastAPI, InfluxDB, Grafana) y cómo interactúan.
- **`DOCKERFILE`**: Configura el contenedor de FastAPI con sus dependencias necesarias.
- **`ENTRYPOINT.SH`**: Automatiza la configuración inicial de InfluxDB, creando buckets, organizaciones y tokens al iniciar el contenedor.
