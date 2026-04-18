<div align="center">

# 🛡️ BlueForge
### Blue Team Training Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat-square&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange?style=flat-square)]()

**La primera plataforma open-source de entrenamiento Blue Team con Docker local, Multi-SIEM integrado y narrativa corporativa real.**

[Ver escenarios](#-escenarios) · [Instalación](#-instalación) · [Arquitectura](#-arquitectura) · [Roadmap](#-roadmap)

</div>

---

## 🎯 ¿Qué es BlueForge?

BlueForge es una plataforma de entrenamiento Blue Team que se despliega en local con Docker. A diferencia de plataformas enfocadas en Red Team, BlueForge sitúa al usuario en el rol de **analista SOC** que llega a una empresa ya comprometida.

Tu misión: investigar qué pasó, cómo y cuándo, usando SIEMs reales con logs pre-generados.

EL ATACANTE YA ENTRÓ. TU ERES EL ANALISTA. EMPIEZA A INVESTIGAR

---

## ✨ Características principales

| Feature | Descripción |
|---|---|
| 🏢 **Narrativa corporativa** | Cada escenario es un incidente en una empresa ficticia real con contexto completo |
| 📊 **Multi-SIEM** | Elastic Stack, Splunk y Wazuh desplegados con un comando |
| 🎯 **Preguntas forenses** | No hay flags clásicas — hay preguntas reales como en un SOC |
| 💡 **Hints progresivos** | 3 niveles de pista por objetivo con coste en puntos |
| 🎫 **Sistema de tickets** | Toma decisiones reales de contención con consecuencias en puntos |
| 📋 **Alert Fatigue** | 40 falsos positivos mezclados con 10 eventos reales — como en producción |
| 🔍 **Shadow IT** | Logs crudos de servidores sin agente SIEM para análisis manual |
| 📚 **Centro educativo** | Guía visual de logs, Event IDs, IOCs y queries SIEM |
| 🐳 **100% Docker** | Un comando levanta todo el entorno — offline, sin cuenta, sin cloud |

---

## 🚀 Instalación

### Requisitos

- Docker Desktop instalado y corriendo
- Python 3.11+
- Git
- 8GB RAM mínimo (16GB recomendado para multi-SIEM)

### Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/mekzzz8/BlueForge.git
cd BlueForge

# 2. Crear entorno virtual e instalar dependencias
python3 -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py && rm get-pip.py
pip install -r requirements.txt

# 3. Inicializar la base de datos
python3 core/init_db.py

# 4. Generar logs del escenario
python3 tools/log_generator.py

# 5. Arrancar BlueForge
python3 core/app.py
```

Abre `http://localhost:5001` en tu navegador.

### Con SIEM integrado

```bash
# Despliegue completo con selector de SIEM
bash core/deploy.sh
```

El script pregunta qué SIEM quieres levantar y lo configura automáticamente.

| SIEM | Puerto | Credenciales |
|---|---|---|
| Kibana (Elastic) | :5601 | Sin auth |
| Splunk | :8000 | admin / BlueForge2025! |
| Wazuh | :443 | admin / admin |

---

## 📋 Escenarios

### SC-001 — Operación NightCrypt
**Empresa:** FinCorp Solutions S.A. · **Tipo:** Ransomware + IR · **Dificultad:** Medium

El 14 de noviembre a las 03:14 UTC el equipo de seguridad de FinCorp detectó actividad anómala. En menos de 20 minutos, el 80% de los ficheros aparecieron cifrados con extensión `.ncrypt`. Reconstruye toda la cadena de ataque.

**Técnicas MITRE ATT&CK:** T1566.001 · T1059.001 · T1547.001 · T1486

**Incluye:**
- ✅ 50 eventos de log (40 ruido + 10 maliciosos)
- ✅ 3 objetivos forenses con hints progresivos
- ✅ 2 tickets de respuesta con penalización por decisiones incorrectas
- ✅ Evidencia Shadow IT — servidor sin agente SIEM
- ✅ SIEM recomendado: Elastic Stack / Splunk

---

### SC-002 — Operación SilentMove *(Próximamente)*
**Empresa:** GovTech Ministerio · **Tipo:** APT + Lateral Movement · **Dificultad:** Hard

### SC-003 — Operación InnerFault *(Próximamente)*
**Empresa:** RetailCorp · **Tipo:** Insider Threat · **Dificultad:** Medium

### SC-004 — Operación ChainBreak *(Próximamente)*
**Empresa:** TechDist · **Tipo:** Supply Chain · **Dificultad:** Hard

---

## 🏗️ Arquitectura

## 🗺️ Roadmap

### v0.1.0 — MVP *(actual)*
- [x] SC-001 Ransomware completo
- [x] Sistema de flags + hints + tickets
- [x] Alert Fatigue + Shadow IT
- [x] Splunk integrado
- [x] Centro educativo de logs

### v0.2.0 *(en desarrollo)*
- [ ] Elastic Stack integrado con dashboards
- [ ] Wazuh integrado con reglas personalizadas
- [ ] SC-002 APT Lateral Movement
- [ ] SC-003 Insider Threat
- [ ] Módulo Phishing SOC con cola de tickets

### v0.3.0 *(planificado)*
- [ ] SC-004 Supply Chain
- [ ] SC-005 Malware Analysis
- [ ] Sistema multiusuario con login
- [ ] Soporte multiidioma (ES/EN)
- [ ] Despliegue en VPS con dominio propio

---

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Python 3.11 + Flask 3.0 |
| Base de datos | SQLite → PostgreSQL |
| Frontend | HTML + CSS + Jinja2 |
| Contenedores | Docker + Compose |
| SIEM 1 | Elastic Stack 8.13 |
| SIEM 2 | Splunk 9.x |
| SIEM 3 | Wazuh 4.7 |
| Log Generator | Python custom |

---

## 📄 Licencia
MIT License
Copyright (c) 2026 Jose Ignacio Navarro de Palencia
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## 👤 Autor

**Jose Ignacio Navarro de Palencia**

Proyecto desarrollado como portfolio de ciberseguridad Blue Team.

---

<div align="center">

**BlueForge** — El atacante ya entró. Tú decides qué pasa después.

⭐ Si te resulta útil, dale una estrella en GitHub

</div>