#!/usr/bin/env bash
set -euo pipefail

TOKEN="$(curl -s http://localhost:8000/api/1/dgii/token | jq -r '.token')"
echo "Token simulado: $TOKEN"

echo "Ejemplo de envío RFCE"
curl -s -X POST http://localhost:8000/api/1/dgii/rfce/send \
  -H "Content-Type: application/json" \
  -d '{"encf":"E310000000001","resumen_xml":"<Resumen/>"}' | jq
