import json
import os
import random
from datetime import datetime, timedelta

BASE_TIME = datetime(2025, 11, 14, 2, 0, 0)
HOST_VICTIMA = "WKSTN-042"
USER_VICTIMA = "j.martinez"
IP_INTERNA = "10.0.0.42"
IP_C2 = "185.220.101.47"

USUARIOS_LEGITIMOS = ["a.garcia", "m.lopez", "p.rodriguez", "c.fernandez", "r.sanchez"]
HOSTS_LEGITIMOS = ["WKSTN-001", "WKSTN-015", "WKSTN-033", "SRV-FILE01", "SRV-PRINT02"]


def generar_timestamp(minutos_offset, variacion=0):
    delta = timedelta(minutes=minutos_offset, seconds=random.randint(0, variacion))
    return (BASE_TIME + delta).isoformat() + "Z"


def generar_ruido(cantidad=40):
    eventos = []
    for i in range(cantidad):
        tipo = random.choice(["login_fallido", "scan_interno", "acceso_archivo", "dns_lookup"])
        usuario = random.choice(USUARIOS_LEGITIMOS)
        host = random.choice(HOSTS_LEGITIMOS)
        offset = random.randint(-120, -1)

        if tipo == "login_fallido":
            eventos.append({
                "timestamp": generar_timestamp(offset, 30),
                "tipo": "login_fallido",
                "host": host,
                "usuario": usuario,
                "event_id": 4625,
                "descripcion": f"Fallo de autenticacion — {usuario} introdujo contrasena incorrecta",
                "es_malicioso": False,
                "fase": "ruido"
            })
        elif tipo == "scan_interno":
            eventos.append({
                "timestamp": generar_timestamp(offset, 60),
                "tipo": "scan_red",
                "host": "SRV-MONITOR01",
                "usuario": "svc_monitor",
                "event_id": 5156,
                "descripcion": "Escaneo de red interno autorizado",
                "es_malicioso": False,
                "fase": "ruido"
            })
        elif tipo == "acceso_archivo":
            eventos.append({
                "timestamp": generar_timestamp(offset, 45),
                "tipo": "acceso_archivo",
                "host": host,
                "usuario": usuario,
                "event_id": 4663,
                "descripcion": "Acceso a fichero compartido — nominas_2025.xlsx",
                "es_malicioso": False,
                "fase": "ruido"
            })
        elif tipo == "dns_lookup":
            dominios = ["office.com", "microsoft.com", "teams.microsoft.com"]
            eventos.append({
                "timestamp": generar_timestamp(offset, 20),
                "tipo": "dns_query",
                "host": host,
                "usuario": usuario,
                "event_id": 22,
                "descripcion": f"Consulta DNS legitima — {random.choice(dominios)}",
                "es_malicioso": False,
                "fase": "ruido"
            })
    return eventos


def generar_ataque_ransomware():
    eventos = []

    eventos.append({
        "timestamp": generar_timestamp(3),
        "tipo": "proceso_creado",
        "host": HOST_VICTIMA,
        "usuario": USER_VICTIMA,
        "event_id": 4688,
        "proceso": "powershell.exe",
        "proceso_padre": "outlook.exe",
        "cmdline": "powershell -enc JABzAD0ATgBlAHcALQBPAGIAagBlAGMAdA==",
        "descripcion": "PowerShell iniciado desde Outlook",
        "es_malicioso": True,
        "fase": "initial_access",
        "mitre": "T1566.001"
    })

    eventos.append({
        "timestamp": generar_timestamp(5),
        "tipo": "conexion_red",
        "host": HOST_VICTIMA,
        "usuario": USER_VICTIMA,
        "event_id": 3,
        "proceso": "powershell.exe",
        "dst_ip": IP_C2,
        "dst_port": 443,
        "bytes": 245760,
        "descripcion": "Descarga payload desde IP externa",
        "es_malicioso": True,
        "fase": "initial_access",
        "mitre": "T1105"
    })

    eventos.append({
        "timestamp": generar_timestamp(7),
        "tipo": "proceso_creado",
        "host": HOST_VICTIMA,
        "usuario": USER_VICTIMA,
        "event_id": 4688,
        "proceso": "svchost_fake.exe",
        "proceso_padre": "powershell.exe",
        "ruta": "C:\\Users\\Public\\svchost_fake.exe",
        "cmdline": "svchost_fake.exe --silent --persist",
        "descripcion": "Proceso sospechoso desde C:\\Users\\Public\\",
        "es_malicioso": True,
        "fase": "execution",
        "mitre": "T1059.001"
    })

    eventos.append({
        "timestamp": generar_timestamp(9),
        "tipo": "modificacion_registro",
        "host": HOST_VICTIMA,
        "usuario": USER_VICTIMA,
        "event_id": 13,
        "clave": "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
        "valor": "svchost_update",
        "dato": "C:\\Users\\Public\\svchost_fake.exe",
        "descripcion": "Modificacion clave Run — persistencia",
        "es_malicioso": True,
        "fase": "persistence",
        "mitre": "T1547.001"
    })

    eventos.append({
        "timestamp": generar_timestamp(12),
        "tipo": "conexion_red",
        "host": HOST_VICTIMA,
        "usuario": USER_VICTIMA,
        "event_id": 3,
        "proceso": "svchost_fake.exe",
        "dst_ip": IP_C2,
        "dst_port": 443,
        "user_agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "bytes": 1240,
        "descripcion": f"Beacon C2 saliente a {IP_C2}",
        "es_malicioso": True,
        "fase": "command_and_control",
        "mitre": "T1071.001"
    })

    for i in range(5):
        eventos.append({
            "timestamp": generar_timestamp(74 + i),
            "tipo": "modificacion_archivo",
            "host": HOST_VICTIMA,
            "usuario": USER_VICTIMA,
            "event_id": 4663,
            "archivo": f"C:\\Datos\\Financiero\\informe_Q{i+1}_2025.xlsx.ncrypt",
            "descripcion": "Archivo cifrado con extension .ncrypt",
            "es_malicioso": True,
            "fase": "impact",
            "mitre": "T1486"
        })

    return eventos


def generar_escenario_completo(output_dir):
    os.makedirs(output_dir, exist_ok=True)

    ruido = generar_ruido(40)
    ataque = generar_ataque_ransomware()
    todos = ruido + ataque
    todos.sort(key=lambda x: x["timestamp"])

    with open(os.path.join(output_dir, "events.json"), "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)

    maliciosos = [e for e in todos if e["es_malicioso"]]
    with open(os.path.join(output_dir, "events_malicious.json"), "w", encoding="utf-8") as f:
        json.dump(maliciosos, f, indent=2, ensure_ascii=False)

    print(f"\n[+] BlueForge — Log Generator")
    print(f"[+] Escenario: Operacion NightCrypt")
    print(f"[+] Total eventos: {len(todos)}")
    print(f"    Ruido (falsos positivos): {len(ruido)}")
    print(f"    Eventos maliciosos reales: {len(ataque)}")
    print(f"[+] Logs guardados en: {output_dir}")


if __name__ == "__main__":
    output = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "scenarios", "sc-001-ransomware", "logs"
    )
    generar_escenario_completo(output)