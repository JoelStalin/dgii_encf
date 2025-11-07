# Política de Seguridad

## Objetivos
- Garantizar integridad, confidencialidad y disponibilidad de los e-CF y derivados.
- Alinear los controles con las normativas DGII, ISO/IEC 27001 y Ley 172-13.

## Controles técnicos
1. **Cifrado**: TLS 1.3 extremo a extremo y cifrado en reposo AES-256 para respaldos.
2. **Gestión de secretos**: almacenados en Vault/KMS; rotación cada 90 días.
3. **Gestión de identidades**: MFA obligatorio, RBAC dinámico y just-in-time access.
4. **Endurecimiento**: imágenes inmutables, escaneo SCA/SAST en CI, parches semanales.
5. **Monitoreo**: logs estructurados en JSON con envío a SIEM y alertas en <5 min.

## Controles administrativos
- Comité de seguridad trimestral.
- Evaluación de proveedores críticos y NDA vigente.
- Matriz de riesgos actualizada mensualmente.

## Gestión de incidentes
1. Detección automática (SIEM) o manual.
2. Clasificación y contención en <30 min.
3. Erradicación y recuperación documentada.
4. Informe a DGII y clientes en <24 h según criticidad.
