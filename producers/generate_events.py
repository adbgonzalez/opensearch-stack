import json
from datetime import datetime, timedelta

endpoints = ["/login", "/logout", "/api/pedidos", "/api/clientes", "/api/facturas", "/api/stock"]
servizos = {
    "/login": "auth",
    "/logout": "auth",
    "/api/pedidos": "pedidos",
    "/api/clientes": "clientes",
    "/api/facturas": "facturacion",
    "/api/stock": "inventario",
}
usuarios = ["ana", "luis", "marta", "xoan", "nerea"]
niveis = ["INFO", "WARN", "ERROR"]

base_date = datetime(2026, 3, 10, 8, 0, 0)  # 10/03/2026 ás 08:00
docs = []

for day in range(10):  # do 10/03 ao 19/03
    current_day = base_date + timedelta(days=day)
    for i in range(10):  # 10 eventos por día
        endpoint = endpoints[(day + i) % len(endpoints)]
        nivel = niveis[(day + i) % len(niveis)]
        usuario = usuarios[(day + i) % len(usuarios)]

        if nivel == "INFO":
            status = 200 if endpoint != "/api/facturas" else 201
            latency = 80 + ((day * 10 + i) % 70)
            mensaxe = "Petición procesada correctamente"
        elif nivel == "WARN":
            status = [401, 403, 429][(day + i) % 3]
            latency = 180 + ((day * 10 + i) % 120)
            mensaxe = "Incidencia leve detectada"
        else:
            status = [500, 502, 504][(day + i) % 3]
            latency = 400 + ((day * 10 + i) % 250)
            mensaxe = "Erro no servizo"

        ts = current_day + timedelta(minutes=i * 75)

        doc = {
            "endpoint": endpoint,
            "ip": f"192.168.{day + 1}.{i + 10}",
            "latency_ms": latency,
            "mensaxe": mensaxe,
            "nivel": nivel,
            "request_id": f"req-{day+1:02d}-{i+1:03d}",
            "servizo": servizos[endpoint],
            "status": status,
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S"),
            "usuario": usuario
        }
        docs.append(doc)

with open("eventos_bulk.ndjson", "w", encoding="utf-8") as f:
    for doc in docs:
        f.write(json.dumps({"index": {"_index": "eventos"}}, ensure_ascii=False) + "\n")
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print(f"Xerados {len(docs)} documentos en eventos_bulk.ndjson")