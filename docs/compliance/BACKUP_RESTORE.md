# Procedimientos de Backup & Restore

## Backup
1. Snapshots incrementales de PostgreSQL (WAL + snapshot completo cada 6 h).
2. Exportación de Redis cada 5 min a almacenamiento S3 con Object Lock (compliance mode, 10 años).
3. XML firmados y acuses se copian a almacenamiento WORM (Glacier Vault Lock) una vez sellados.
4. Verificación diaria de integridad (hash SHA-512 + hash-chain) y reporte al SIEM.

## Restore
1. Solicitud aprobada por CISO + CTO.
2. Selección del punto en el tiempo usando catálogos de snapshots.
3. Restauración automatizada via Terraform + scripts `ops/restore_ecf.py`.
4. Validación por QA (checksums y XSD) antes de abrir a usuarios.
5. Documentación en BITACORA.md e informe DGII si aplica.
