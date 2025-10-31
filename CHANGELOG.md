# Changelog

## [Unreleased]
- Inicialización del historial de cambios.

## [DGII e-CF: firma SHA-256, clientes, XSD, RI, CI y guía]
- Incorporación de cliente DGII con autenticación, recepción y consultas resilientes.
- Implementación de firma XMLDSig RSA-SHA256 y validación XSD para e-CF y documentos relacionados.
- Nuevos routers FastAPI (`/api/dgii/*`, `/ri/*`) con representación impresa y QR.
- Pruebas unitarias, contractuales y de extremo a extremo con cobertura ≥ 85%.
- Dockerfile slim, docker-compose, Makefile y workflow CI (ruff, mypy, pytest, build).
- Documentación completa: guía de implementación, seguridad del proveedor, README actualizado.
