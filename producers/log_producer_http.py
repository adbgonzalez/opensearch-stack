import time
import random
import requests
from datetime import datetime, timezone

# Lista de servizos "simulados" para etiquetar cada evento de log.
SERVICES = ["auth", "api", "db", "payments"]

# Niveis posibles do log (informativo, aviso, erro).
LEVELS = ["info", "warn", "error"]

# Endpoint de Data Prepper ao que se enviarán os eventos de logs.
DATAPREPPER_URL = "http://data-prepper:2022/events/logs"

def now_utc_iso():
    """
    Devolve a hora actual en UTC en formato ISO 8601.
    Substitúe '+00:00' por 'Z' para indicar explicitamente UTC.
    Ex.: 2026-02-26T12:34:56.789012Z
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Bucle infinito: xera un evento de log aleatorio e envíao periodicamente a Data Prepper.
while True:
    # Constrúe un evento de log sintético con campos típicos.
    evento = {
        # Timestamp de creación do evento (inxestión no producer).
        "timestamp": now_utc_iso(),

        # Nome do servizo ao que se lle atribúe o log (escollido ao azar).
        "servizo": random.choice(SERVICES),

        # Nivel do log (info/warn/error) escollido ao azar.
        "nivel": random.choice(LEVELS),

        # Latencia simulada (en milisegundos), xerada ao azar entre 10 e 1000.
        "latency_ms": random.randint(10, 1000)
    }

    try:
        # Envía o evento por POST como JSON ao endpoint de Data Prepper.
        # Vaise nunha lista [evento] para manter o formato "batch" (aínda que sexa dun só elemento).
        # Timeout de 5 segundos para evitar quedar bloqueado se o receptor non responde.
        resp = requests.post(DATAPREPPER_URL, json=[evento], timeout=5)

        # Log por consola do status HTTP devolto e do evento que se intentou enviar.
        print("status:", resp.status_code, "| enviado:", evento)
    except Exception as e:
        # Captura erros de rede/timeout, etc., e móstraos por consola.
        print("erro:", e)

    # Agarda 2 segundos antes de xerar e enviar o seguinte evento.
    time.sleep(2)