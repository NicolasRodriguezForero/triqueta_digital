# Resumen de Funcionalidades Backend Pendientes

> Alcance: funcionalidades no implementadas después de la finalización del Sprint 2. Fuente principal: Cronograma Simplificado y lista de tareas pendientes.

## Sprint 3 · Actividades (Parte 2) + Admin

- Servicio de importación de actividades (`activity_import_service.py`).
- Parsers CSV y JSON con validaciones completas.
- Detección de duplicados (título, fecha, ubicación) en importaciones.
- Endpoint `POST /admin/actividades/import`.
- Gestión de estados de actividad (`activa`, `pendiente_validacion`, `rechazada`).
- Endpoints administrativos para aprobar/rechazar actividades (`POST /admin/actividades/{id}/aprobar`, `POST /admin/actividades/{id}/rechazar`).

## Sprint 4 · Favoritos + Recomendaciones IA (MVP)

- Modelo `Favorite` con relaciones usuario-actividad.
- Endpoints CRUD de favoritos (`POST/GET/DELETE /favoritos`).
- Actualización de métricas de popularidad al gestionar favoritos.
- Servicio de recomendaciones (`recommendation_service.py`).
- Algoritmo híbrido (popularidad, etiquetas, localidad, disponibilidad) con explicaciones.
- Endpoint `GET /recomendaciones`.
- Caché de recomendaciones en Redis.
- Job diario para recalcular `popularidad_normalizada`.

## Sprint 5 · Dashboard Admin

- Endpoint `GET /admin/dashboard` con métricas y caché.
- Consultas agregadas: usuarios totales/activos/nuevos, actividades por localidad/tipo, top 10 actividades y etiquetas.
- Gestión de usuarios administradores (endpoints `GET /admin/usuarios`, `PATCH /admin/usuarios/{id}/rol`, `PATCH /admin/usuarios/{id}/estado`).

## Sprint 6 · ETL + Importación Automatizada

- Modelo `ETLExecution` para registrar ejecuciones.
- Endpoints de estado/ejecución/logs del ETL (`GET /admin/etl/status`, `POST /admin/etl/run`, `GET /admin/etl/executions/{id}/logs`).
- Integración de SSE o polling para transmisión de logs.
- Script ETL en `/etl/src/` con extractores (IDRD, Portales Distritales), transformaciones y carga en PostgreSQL.
- Detección de duplicados y logging integral dentro del ETL.
- Dockerfile específico y configuración Docker Compose para el servicio ETL.

## Sprint 7 · Testing Final + Deployment

- Validación de índices de base de datos y optimización de consultas.
- Implementación de rate limiting en los endpoints públicos restantes.
- Pruebas de performance de API y optimizaciones correspondientes.
- Cobertura mínima de tests (>80% backend) y refactors resultantes.
- Seguridad: SAST (Bandit/Semgrep), dependency checks.
- Automatización CI/CD completa en GitHub Actions.
- Preparación y ejecución de deploy final a producción (servidores, monitoreo, backups).
- Actualización final de documentación (API, Deployment, README).
