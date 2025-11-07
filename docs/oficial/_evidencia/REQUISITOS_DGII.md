# Matriz de Requisitos de Cumplimiento DGII e-CF

La siguiente matriz consolida los requisitos identificados en la documentación oficial. El estado `Pendiente` indica que aún no se ha implementado la verificación en el código base; las citas permiten volver al documento fuente.

## Firma XMLDSig

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| FIR-01 | Usar `SignatureMethod` RSA-SHA256 en la firma enveloped. | `[Firmado de e-CF.pdf, p.5]` | Pendiente | La guía de firmado muestra el algoritmo requerido en el ejemplo de `<SignedInfo>`. |
| FIR-02 | Calcular `DigestMethod` con SHA-256. | `[Firmado de e-CF.pdf, p.5]` | Pendiente | El ejemplo de referencia señala `DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"`. |
| FIR-03 | Definir `Reference URI=""` para firmar el documento completo. | `[Firmado de e-CF.pdf, p.5]` | Pendiente | La plantilla de firma establece una referencia vacía sobre el documento. |
| FIR-04 | Aplicar Canonicalización C14N sin comentarios. | `[Firmado de e-CF.pdf, p.5]` | Pendiente | El XML de muestra utiliza `CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"`. |
| FIR-05 | Firmar sin preservar espacios (`preserveWhiteSpace = false`). | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.60]` | Pendiente | La guía técnica indica deshabilitar `preserveWhiteSpace` al firmar. |

## Validación XSD

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| XSD-01 | Validar cada tipo de e-CF (31-47) contra su XSD oficial. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.4]` | Pendiente | La tabla inicial enumera los formatos e-CF disponibles y sus XSD de referencia. |
| XSD-02 | Validar ARECF, ACECF, ANECF y RFCE contra sus XSD. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.4]` | Pendiente | El mismo cuadro incluye los artefactos de receptor y el RFCE. |
| XSD-03 | Mantener versiones y checksums de los XSD. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.4]` | Pendiente | Se requiere control de integridad; actualmente el repositorio ya conserva hashes en `xsd_inventory.json`. |

## Representación Impresa y QR

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| RI-01 | Incluir todos los campos marcados como “I/P” en la RI. | `[Representación Impresa (Modelos ilustrativos).pdf, p.1]` | Pendiente | Los modelos ilustrativos muestran los campos impresos; se requiere derivar explícitamente la lista I/P (OCR pendiente para detalle). |
| RI-02 | Generar QR con versión 8 y URL oficial de consulta. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.41]` | Pendiente | La guía especifica la versión del código QR y los parámetros que deben exponerse. |
| RI-03 | Incluir el código de seguridad en el QR y en la RI. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.25][Descripcion-tecnica-de-facturacion-electronica.pdf, p.41]` | Pendiente | Los servicios de consulta requieren el código de seguridad, por lo que debe aparecer en el QR e impresión. |

## Mensajería del Receptor

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| REC-01 | Emitir ARECF para confirmar recepción (obligatorio). | `[Formato Acuse de Recibo v 1.0.pdf, p.2]` | Pendiente | El documento indica que el receptor debe enviar acuse en cada recepción. |
| REC-02 | Enviar ACECF (aprobación/rechazo) y remitir copia a la DGII. | `[Formato Aprobación Comercial v1.0.pdf, p.2]` | Pendiente | Se establece la obligación de enviar la respuesta comercial y copia a la DGII. |
| REC-03 | Gestionar ANECF para anular secuencias no usadas. | `[Formato Anulación de e-NCF v1.0.pdf, p.3]` | Pendiente | Describe cuándo emitir ANECF y la obligación de firmar el archivo. |

## RFCE (< RD$ 250,000)

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| RFC-01 | Aplicar umbral de RD$ 250,000 para resumen de consumo. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.4][Formato Resumen Factura Consumo Electrónica v1.0.pdf, p.1]` | Pendiente | Ambos documentos fijan el límite y el formato que debe enviarse. |
| RFC-02 | Validar estructura, longitudes y catálogos del RFCE. | `[Formato Resumen Factura Consumo Electrónica v1.0.pdf, p.3]` | Pendiente | Se detallan longitudes, tipos y códigos de ingresos. |
| RFC-03 | Enviar RFCE a la DGII y manejar la respuesta. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.14][Descripcion-tecnica-de-facturacion-electronica.pdf, p.17]` | Pendiente | La guía incluye los endpoints de recepción y la respuesta de validación. |

## Cliente DGII (Servicios)

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| CLI-01 | Implementar flujo `semilla → validación → token`. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.10][Descripcion-tecnica-de-facturacion-electronica.pdf, p.58]` | Pendiente | Se documentan los recursos `/autenticacion/api/semilla` y la validación del certificado para obtener el token. |
| CLI-02 | Implementar consultas (directorio, trackId, resultado, resúmenes). | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.18][Descripcion-tecnica-de-facturacion-electronica.pdf, p.29][Descripcion-tecnica-de-facturacion-electronica.pdf, p.37]` | Pendiente | La guía especifica URLs y parámetros para cada consulta oficial. |
| CLI-03 | Manejar la regla de reutilización de eNCF y secuencias. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.24]` | Pendiente | Las respuestas de validación incluyen mensajes sobre secuencias vencidas o reutilizadas; se requiere lógica de manejo. |
| CLI-04 | Configurar URLs por ambiente (Pre-Cert, Certificación, Producción). | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.13]` | Pendiente | Se listan las URLs base específicas por ambiente para recepción y consultas. |

## Generales y Seguridad

| ID | Requisito | Fuente(s) [PDF, p.X] | Estado | Comentario |
| --- | --- | --- | --- | --- |
| GEN-01 | Aplicar estándar de nombres de archivo oficial. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.63]` | Pendiente | Incluye patrón `RNC+Tipo+Secuencia` y restricción de caracteres prohibidos. |
| GEN-02 | Usar codificación UTF-8 en todos los XML. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.27]` | Pendiente | Los ejemplos de respuesta y solicitud en la guía declaran `encoding="UTF-8"`. |
| GEN-03 | Rechazar tags vacíos o longitudes fuera de rango. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.63]` | Pendiente | La guía indica explícitamente que no deben existir tags vacíos en los XML. |
| SEC-01 | Documentar políticas de seguridad, contingencia y privacidad (Ley 172-13). | `[Proceso Certificacion para ser Proveedor de Servicios eCF.pdf, p.5]` | Pendiente | El proceso de certificación exige contar con infraestructura, delegaciones y controles; se requiere ampliar la política formal (no detallada en el PDF, preparar plan interno). |
| SEC-02 | Mantener bitácora de eventos y auditoría. | `[Descripcion-tecnica-de-facturacion-electronica.pdf, p.52]` | Pendiente | El servicio de monitoreo expone estados de disponibilidad; se debe complementar con bitácoras propias (detalle específico no provisto). |
| SEC-03 | Gestionar backups y plan de restauración. | `[Proceso Certificacion para ser Proveedor de Servicios eCF.pdf, p.5]` | Pendiente | El documento exige demostrar capacidad operativa continua; se requiere plan de respaldo explícito (detalle adicional pendiente). |

## Observaciones

- Algunos requisitos (RI-01 y SEC-01/SEC-03) dependen de contenido gráfico o referencias implícitas; se requiere OCR o lineamientos adicionales de la DGII para documentar la evidencia completa.
- La matriz se actualizará conforme se implementen validadores y pruebas automatizadas en el repositorio.
