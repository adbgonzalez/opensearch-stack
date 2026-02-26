import os
import time
import requests
from datetime import datetime, timezone

# ID da rede en CityBikes (p.ex. "bicimad"). Se non existe a variable de contorno,
# úsase "bicimad" por defecto.
CITYBIKES_NETWORK_ID = os.getenv("CITYBIKES_NETWORK_ID", "bicimad")

# URL do endpoint da API de CityBikes para consultar a rede indicada.
CITYBIKES_URL = f"https://api.citybik.es/v2/networks/{CITYBIKES_NETWORK_ID}"

# Endpoint de Data Prepper ao que se enviarán os eventos xerados.
DATAPREPPER_URL = "http://data-prepper:2021/events/bikes"

# Intervalo de consulta en segundos. Por defecto 60s se non se define POLL_SECONDS.
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "60"))

# Timeout HTTP (en segundos) para as peticións GET/POST. Por defecto 10s.
TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "10"))

def now_utc_iso():
    """
    Devolve a hora actual en UTC en formato ISO 8601.
    Converte o sufixo +00:00 a 'Z' para indicar explicitamente UTC.
    Ex.: 2026-02-26T12:34:56.789012Z
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Mensaxe inicial de arranque: indica rede, intervalo de polling e destino de envío.
print(f"[citybikes] network={CITYBIKES_NETWORK_ID} poll={POLL_SECONDS}s -> {DATAPREPPER_URL}")

# Bucle infinito: consulta periódica a CityBikes e envío dos datos a Data Prepper.
while True:
    try:
        # Solicitude GET á API de CityBikes para obter o estado actual da rede.
        r = requests.get(CITYBIKES_URL, timeout=TIMEOUT)

        # Lanza excepción se o status HTTP é de erro (4xx/5xx).
        r.raise_for_status()

        # Parseo da resposta JSON.
        data = r.json()

        # O obxecto raíz trae unha chave "network" cos metadatos da rede e estacións.
        network = data.get("network", {})

        # Lista de estacións dentro da rede. Se non existe, queda como lista baleira.
        stations = network.get("stations", [])

        # Timestamp común (instante de inxestión) para todos os eventos xerados neste ciclo.
        ts = now_utc_iso()

        # Lista onde se acumularán os eventos (un por estación) a enviar a Data Prepper.
        eventos = []

        # Para cada estación da rede, constrúese un evento coas métricas principais.
        for st in stations:
            eventos.append({
                # Timestamp de cando se xera/recopila o evento (inxestión no producer).
                "timestamp": ts,

                # Identifica a orixe dos datos (neste caso, a API citybik.es).
                "orixe": "citybik.es",

                # Identificador da rede consultada (o que se pasou na URL).
                "network_id": CITYBIKES_NETWORK_ID,

                # Nome human-readable da rede (se vén no JSON).
                "network_name": network.get("name"),

                # Identificador da estación (segundo CityBikes).
                "station_id": st.get("id"),

                # Nome da estación.
                "station_name": st.get("name"),

                # Bicis dispoñibles nese momento na estación.
                "free_bikes": st.get("free_bikes"),

                # Ocupación inversa: slots libres para deixar bicis.
                "empty_slots": st.get("empty_slots"),

                # Coordenadas xeográficas da estación.
                "latitude": st.get("latitude"),
                "longitude": st.get("longitude"),

                # Timestamp "last updated" da estación segundo o provedor (pode ser epoch/segundos).
                "last_updated": st.get("timestamp"),
            })

        # Envío por POST de toda a lista de eventos como JSON ao endpoint de Data Prepper.
        resp = requests.post(DATAPREPPER_URL, json=eventos, timeout=TIMEOUT)

        # Log básico: cantos eventos se enviaron e status HTTP do receptor.
        print(f"[citybikes] enviados {len(eventos)} | status={resp.status_code}")

        # Se o status indica redirección/erro (>=300), amósase un anaco do corpo da resposta.
        if resp.status_code >= 300:
            print(resp.text[:200])

    except Exception as e:
        # Captura calquera excepción (rede, JSON, status HTTP, etc.) e rexístrase por consola.
        print("[citybikes] erro:", repr(e))

    # Agarda o intervalo configurado antes de repetir o ciclo.
    time.sleep(POLL_SECONDS)