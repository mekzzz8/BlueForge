#!/bin/bash

BLUE='\033[0;34m'
GREEN='\033[0;32m'
AMBER='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           B L U E F O R G E  v0.1               ║${NC}"
echo -e "${BLUE}║        Blue Team Training Platform               ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
echo ""

LAB_IP="localhost"

echo -e "${AMBER}[?] Selecciona el SIEM para este escenario:${NC}"
echo ""
echo "  1) Elastic Stack (Kibana) — Recomendado para SC-001"
echo "  2) Splunk                 — Recomendado para SC-002"
echo "  3) Wazuh                  — Recomendado para SC-003"
echo "  4) Solo BlueForge (sin SIEM)"
echo ""
read -p "  Opción [1-4]: " SIEM_CHOICE

echo ""
echo -e "${AMBER}[*] Generando logs del escenario...${NC}"
python3 tools/log_generator.py

echo -e "${AMBER}[*] Desplegando contenedores...${NC}"
echo ""

case $SIEM_CHOICE in
    1)
        docker compose -f docker-compose.yml \
                       -f siem/docker-compose.elastic.yml \
                       up -d --build
        SIEM_NAME="Elastic Stack"
        SIEM_URL="http://$LAB_IP:5601"
        ;;
    2)
        docker compose -f docker-compose.yml \
                       -f siem/docker-compose.splunk.yml \
                       up -d --build
        SIEM_NAME="Splunk"
        SIEM_URL="http://$LAB_IP:8000"
        ;;
    3)
        docker compose -f docker-compose.yml \
                       -f siem/docker-compose.wazuh.yml \
                       up -d --build
        SIEM_NAME="Wazuh"
        SIEM_URL="https://$LAB_IP:443"
        ;;
    4)
        docker compose -f docker-compose.yml up -d --build
        SIEM_NAME="Ninguno"
        SIEM_URL="—"
        ;;
    *)
        echo -e "${RED}[!] Opción inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ BlueForge desplegado correctamente${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Panel BlueForge: ${BLUE}http://$LAB_IP:5001${NC}"
echo -e "  SIEM activo:     ${BLUE}$SIEM_URL${NC} ($SIEM_NAME)"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  Escenario activo: ${AMBER}Operación NightCrypt${NC}"
echo -e "  Empresa víctima:  FinCorp Solutions S.A."
echo -e "  Dificultad:       MEDIUM"
echo ""
echo -e "  Credenciales Splunk: admin / BlueForge2025!"
echo ""