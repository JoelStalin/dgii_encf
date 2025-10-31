# DGII e-CF — Guía de Implementación

Esta guía describe el proceso completo para integrar la plataforma con los servicios de facturación electrónica de la DGII. Los ejemplos utilizan Python 3.12, FastAPI y el cliente `DGIIClient` incluido en este repositorio.

## 1. Requisitos previos

- Python 3.12 o superior y `pip`
- OpenSSL ≥ 1.1 para la gestión de certificados
- Certificado digital en formato `.p12`/`.pfx` emitido por la DGII
- Cuenta activa en los ambientes de Pre-Certificación, Certificación y Producción
- Docker 24+ (opcional para despliegue contenedorizado)

## 2. Configuración del `.env`

Copia el archivo `.env.example` y especifica los valores para cada ambiente:

```bash
cp .env.example .env.development
```

Variables clave:

- `ENV`: Ambiente objetivo (`PRECERT`, `CERT`, `PROD`)
- `DGII_AUTH_BASE_URL_*`, `DGII_RECEPCION_BASE_URL_*`, `DGII_RECEPCION_FC_BASE_URL_*`, `DGII_DIRECTORIO_BASE_URL_*`: URLs provistas por DGII
- `DGII_RNC`: RNC del emisor
- `DGII_CERT_P12_PATH` y `DGII_CERT_P12_PASSWORD`: Ruta segura y contraseña del certificado
- `DGII_HTTP_TIMEOUT_SECONDS` y `DGII_HTTP_RETRIES`: Configuración de resiliencia
- `RI_QR_BASE_URL`: Base del URL que se codificará en el QR de la RI

## 3. Firmar y verificar un e-CF

```python
from pathlib import Path

from app.dgii.signing import sign_ecf
from app.dgii.validation import validate_xml

xml_bytes = Path("samples/ecf_valid.xml").read_bytes()
validate_xml(xml_bytes, "ECF.xsd")
signed = sign_ecf(xml_bytes, "/secrets/company_cert.p12", "********")
Path("ecf_signed.xml").write_bytes(signed)
```

Verifica la firma utilizando `signxml`:

```python
from cryptography.hazmat.primitives import serialization
from signxml import XMLVerifier
from lxml import etree

cert = ...  # carga del certificado X.509 en DER
XMLVerifier().verify(signed, x509_cert=cert.public_bytes(serialization.Encoding.DER))
```

## 4. Consumir los endpoints DGII

Obtén el token:

```bash
http POST :8000/api/dgii/auth/token
```

Envía un e-CF firmado:

```bash
http POST :8000/api/dgii/recepcion/ecf \
  "Authorization:Bearer <token>" \
  encf=E310000000001 tipoECF=E31 rncEmisor=131415161 \
  rncReceptor=172839405 fechaEmision="2024-05-01T10:00:00Z" montoTotal:=1500 \
  items:='[{"descripcion": "Servicio", "cantidad": 1, "precioUnitario": 1500}]'
```

Consulta el estado del track ID:

```bash
http GET :8000/api/dgii/recepcion/status/TRACK-123 "Authorization:Bearer <token>"
```

## 5. Generar Representación Impresa con QR

```bash
http POST :8000/ri/render formato==both \
  encf=E310000000001 rncEmisor=131415161 razonSocialEmisor="Empresa Demo" \
  rncReceptor=172839405 razonSocialReceptor="Cliente Demo" montoTotal:=1500 \
  items:='[{"descripcion": "Servicio", "cantidad": 1, "precioUnitario": 1500}]'
```

La respuesta contiene el HTML listo para imprimir y el PDF codificado en base64. El QR se genera usando la URL configurada en `RI_QR_BASE_URL`.

## 6. Flujo de certificación — Checklist

1. Configurar los endpoints para el ambiente `PRECERT`
2. Ejecutar pruebas unitarias y contract tests (`make test`)
3. Validar RI con datos reales y QR de homologación
4. Registrar cada envío en bitácora interna con `track_id` y `request_id`
5. Enviar lotes de pruebas a la DGII y recopilar acuses/observaciones
6. Migrar variables a `CERT` y repetir pruebas
7. Documentar evidencias solicitadas por la DGII (tokens, track IDs, logs)
8. Desplegar en Producción solo después de recibir la aprobación formal

## 7. Troubleshooting

| Problema | Causa probable | Resolución |
| --- | --- | --- |
| `Se requiere el comando 'poetry'` | Dependencia faltante | Ejecuta `scripts/install.sh` para instalar Poetry automáticamente |
| Firma inválida | Contraseña o certificado incorrecto | Verifica la ruta `DGII_CERT_P12_PATH` y la contraseña |
| Respuesta 5xx de DGII | Intermitencia en servicio | El cliente reintenta automáticamente; revisa logs y reintenta manualmente si persiste |
| XSD no encontrado | Archivos faltantes en `schemas/` | Ejecuta `poetry run pytest tests/test_validation.py` para validar instalación |
| QR incorrecto | URL base mal configurada | Actualiza `RI_QR_BASE_URL` en el `.env` |
