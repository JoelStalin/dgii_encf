# Matriz de Requisitos de Cumplimiento DGII e-CF

Este documento consolida los requisitos técnicos y de cumplimiento para la facturación electrónica en República Dominicana, según la documentación oficial de la DGII.

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| -- | --------- | -------------------- | ------ | ---------- |
| **Firma XMLDSig** |
| FIR-01 | Algoritmo `RSA-SHA256` | `[Firmado de e-CF.pdf, p.X]` | `Pendiente` | |
| FIR-02 | `DigestMethod` debe ser `SHA256` | `[Firmado de e-CF.pdf, p.X]` | `Pendiente` | |
| FIR-03 | `Reference URI` debe ser `""` (documento completo) | `[Firmado de e-CF.pdf, p.X]` | `Pendiente` | |
| FIR-04 | Aplicar Canonicalización (C14N) | `[Firmado de e-CF.pdf, p.X]` | `Pendiente` | |
| FIR-05 | XML no debe contener comentarios | `[Firmado de e-CF.pdf, p.X]` | `Pendiente` | |
| **Validación XSD** |
| XSD-01 | Validar cada tipo de e-CF (31-47) contra su XSD | `[e-CF 31 v.1.0.xsd]` | `Pendiente` | La estructura base del e-CF está definida. Se necesita validar la obligatoriedad de campos condicionales. |
| XSD-02 | Validar mensajes ARECF, ACECF, ANECF, RFCE | `[ARECF v1.0.xsd]` | `Pendiente` | El XSD del ARECF define los campos `RNCEmisor`, `RNCComprador`, `eNCF`, `Estado`, `FechaHoraAcuseRecibo` y `CodigoMotivoNoRecibido`. |
| XSD-03 | Mantener checksums y versiones de XSD | `[Internal]` | `En Progreso` | Las versiones de los XSD han sido inventariadas en `xsd_inventory.json`. |
| **Representación Impresa (RI) y QR** |
| RI-01 | Incluir todos los campos marcados como "I/P" | `[Representación Impresa (Modelos ilustrativos).pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para identificar los campos "I/P". |
| RI-02 | URL del QR debe ser correcta y apuntar a la consulta | `[Representación Impresa (Modelos ilustrativos).pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para conocer el formato de la URL. |
| RI-03 | QR debe contener el código de seguridad correcto | `[Representación Impresa (Modelos ilustrativos).pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para conocer la estructura del código de seguridad. |
| **Mensajería del Receptor** |
| REC-01 | ARECF es siempre obligatorio | `[Formato Acuse de Recibo v 1.0.pdf, p.X]` | `Pendiente` | Confirmado a través de la existencia de `ARECF v1.0.xsd`. |
| REC-02 | ACECF es condicional y se envía copia a DGII | `[Formato Aprobación Comercial v1.0.pdf, p.X]` | `Pendiente` | Se requiere el PDF para entender las condiciones. |
| REC-03 | ANECF se usa para el flujo de anulación | `[Formato Anulación de e-NCF v1.0.pdf, p.X]` | `Pendiente` | Se requiere el PDF para entender el flujo. |
| **RFCE (Resumen de Factura de Consumo)** |
| RFC-01 | Umbral de monto < RD$ 250,000 | `[Formato Resumen Factura Consumo Electrónica v1.0.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para confirmar el umbral. |
| RFC-02 | Estructura, longitudes y validaciones según formato | `[RFCE 32 v.1.0.xsd]` | `Pendiente` | El XSD define la estructura, pero se necesita el PDF para reglas de negocio adicionales. |
| RFC-03 | Envío a DGII y manejo de respuesta | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para los detalles del endpoint y el manejo de la respuesta. |
| **Cliente DGII (Servicios)** |
| CLI-01 | Flujo Semilla -> Token -> Envío | `[Semilla v.1.0.xsd]` | `Pendiente` | La estructura de la semilla está definida en el XSD. El flujo completo requiere el PDF. |
| CLI-02 | Consultas: Directorio, TrackID, Resultado, Resúmenes | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para los detalles de los endpoints y los formatos de los mensajes. |
| CLI-03 | Manejo de secuencias y "reutilizar eNCF" | `[Internal - a definir]` | `Pendiente` | Este requisito parece ser interno y necesita más definición. |
| CLI-04 | URLs separadas por ambiente (Pre-cert, Cert, Prod) | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para obtener las URLs de cada ambiente. |
| **Generales y de Seguridad** |
| GEN-01 | Nombres de archivo según estándar oficial | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para conocer el estándar de nombres de archivo. |
| GEN-02 | Codificación de archivos debe ser UTF-8 | `[e-CF 31 v.1.0.xsd]` | `Pendiente` | El encabezado del XSD (`<?xml version="1.0" encoding="utf-8" ?>`) confirma el uso de UTF-8. |
| GEN-03 | Rechazar tags vacíos o con longitudes fuera de rango | `[e-CF 31 v.1.0.xsd]` | `Pendiente` | Las longitudes y los tipos de datos están definidos en los XSD. Se necesita implementar un validador que los aplique. |
| SEC-01 | Políticas de seguridad, contingencia, privacidad (Ley 172-13) | `[Proceso Certificacion para ser Proveedor de Servicios eCF.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para conocer las políticas específicas. |
| SEC-02 | Bitácora de eventos y auditoría | `[Proceso Certificacion para ser Proveedor de Servicios eCF.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para conocer los requisitos de la bitácora. |
| SEC-03 | Backups y plan de restauración | `[Proceso Certificacion para ser Proveedor de Servicios eCF.pdf, p.X]` | `Pendiente` | **BLOQUEADO:** Se requiere el PDF para conocer los requisitos de backup y restauración. |
