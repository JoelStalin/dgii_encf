# Plan de Continuidad y Contingencia

## Metas
- RPO: 5 minutos.
- RTO: 30 minutos para servicios críticos (autenticación y recepción).

## Estrategia
1. **Infraestructura activa/activa** en dos regiones (Santo Domingo y Virginia).
2. **Backups incrementales** cada 5 min hacia almacenamiento WORM.
3. **Failover automático** mediante orquestador y healthchecks.
4. **Pruebas trimestrales** de DRP con checklist firmado.

## Procedimiento resumido
1. Declarar evento y notificar a DGII + clientes.
2. Activar sitio secundario vía Terraform + ArgoCD.
3. Restaurar colas pendientes desde Redis/Aurora snapshots.
4. Validar integridad (hash-chain) antes de reabrir el tráfico.
