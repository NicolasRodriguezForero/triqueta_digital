# Tareas Pendientes Triqueta Digital (Post-Sprint 2)

> Referencia: Sprint 2 completado al 100%. Organización en 3 sprints semanales para culminar el MVP y preparar la entrega final. Responsables asignados por rol principal.

## Roles

- **PM**: Coordinación general, seguimiento y soporte multiplataforma.
- **Backend Lead**: Servicios FastAPI, lógica de negocio y persistencia.
- **Frontend Lead**: UI/UX en React, manejo de estado y componentes.
- **Data/ETL Lead**: Ingesta, validaciones de datos y automatización ETL.
- **QA/DevOps Lead**: Pruebas, CI/CD, performance y despliegues.

---

## Sprint 3 (Semana 1) · Favoritos + Recomendaciones IA (MVP)

### Backend

| Tarea                                    | Descripción                                                                                                                                                                                                 | Responsable                   |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Endpoints CRUD favoritos**             | Implementar `POST /favoritos` (agregar), `GET /favoritos` (listar con paginación y filtros), `DELETE /favoritos/{id}` (eliminar) con autenticación requerida.                                               | Backend Lead                  |
| **Actualización métricas popularidad**   | Incrementar/decrementar contador de favoritos en tabla actividades al agregar/quitar favorito, impactando el score de popularidad para recomendaciones.                                                     | Backend Lead                  |
| **Servicio `recommendation_service.py`** | Implementar servicio con algoritmo híbrido que combine: popularidad normalizada, coincidencia de etiquetas, proximidad de localidad, y disponibilidad de fechas. Incluir lógica de scoring y explicaciones. | Backend Lead + Data/ETL Lead  |
| **Endpoint `GET /recomendaciones`**      | Exponer endpoint que devuelva top N actividades recomendadas con explicaciones personalizadas (ej: "Popular en tu localidad", "Basado en tus favoritos").                                                   | Backend Lead                  |
| **Caching Redis recomendaciones**        | Implementar cache por usuario con TTL de 1 hora para optimizar performance de recomendaciones. Invalidar cache al agregar/quitar favoritos.                                                                 | Backend Lead                  |
| **Job diario popularidad**               | Crear tarea programada (APScheduler o Celery) que recalcule `popularidad_normalizada` basado en views, favoritos y fecha de última actualización.                                                           | Backend Lead + QA/DevOps Lead |

### Frontend

| Tarea                                                   | Descripción                                                                                                                                         | Responsable    |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **Servicios API `favorites.ts` y `recommendations.ts`** | Crear servicios con tipado completo para endpoints de favoritos y recomendaciones, incluyendo tipos TypeScript para request/response.               | Frontend Lead  |
| **Hooks React Query favoritos**                         | Implementar `useFavorites` (query), `useAddFavorite` (mutation), `useRemoveFavorite` (mutation) con optimistic updates e invalidación de cache.     | Frontend Lead  |
| **Hook `useRecommendations`**                           | Crear hook que consuma endpoint de recomendaciones con manejo de estados (loading, error, empty) y refetch automático.                              | Frontend Lead  |
| **Componente `FavoriteButton`**                         | Botón toggle con ícono corazón, estados visuales (lleno/vacío), control optimista, feedback visual (animación, toast) y manejo de errores.          | Frontend Lead  |
| **Integración en `ActivityCard`**                       | Agregar `FavoriteButton` en esquina superior derecha de tarjetas en listados y detalle, con lógica de autenticación requerida.                      | Frontend Lead  |
| **Página `/favoritos`**                                 | Listado de actividades favoritas con filtros básicos (tipo, localidad), estado vacío con call-to-action, paginación y acceso rápido al detalle.     | Frontend Lead  |
| **Página `/recomendaciones`**                           | Grid de actividades recomendadas con tarjetas que muestren explicación personalizada, ordenamiento por score, y posibilidad de agregar a favoritos. | Frontend Lead  |
| **Tests favoritos/recomendaciones**                     | Unit tests de hooks y componentes, E2E con Playwright del flujo completo: agregar/quitar favorito, ver lista, recibir recomendaciones.              | QA/DevOps Lead |

### Coordinación

| Tarea                                 | Responsable    |
| ------------------------------------- | -------------- |
| Deploy del MVP en staging             | QA/DevOps Lead |
| Coordinación de demo interna MVP      | PM             |
| Seguimiento y comunicación del sprint | PM             |

---

## Sprint 4 (Semana 2) · Dashboard Admin + ETL + Validación

### Backend

| Tarea                               | Descripción                                                                                                                                                                                                 | Responsable                    |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **Endpoint `GET /admin/dashboard`** | Crear endpoint que devuelva métricas agregadas: usuarios (total, activos, nuevos), actividades (por localidad, por tipo, por estado), top 10 actividades y etiquetas. Implementar cache Redis de 5 minutos. | Backend Lead                   |
| **Queries agregadas optimizadas**   | Implementar queries SQL eficientes usando GROUP BY, COUNT, agregaciones, con índices apropiados para performance en dashboard.                                                                              | Backend Lead                   |
| **Gestión usuarios admin**          | Endpoints `GET /admin/usuarios` (lista con filtros/paginación), `PATCH /admin/usuarios/{id}/rol` (cambiar rol), `PATCH /admin/usuarios/{id}/estado` (activar/desactivar) con validaciones y permisos.       | Backend Lead                   |
| **Modelo `ETLExecution`**           | Crear modelo para registrar ejecuciones ETL: timestamp inicio/fin, estado (running/success/failed), contador de registros procesados/insertados/actualizados/errores, logs almacenados.                     | Backend Lead                   |
| **Endpoints gestión ETL**           | Implementar `GET /admin/etl/status` (estado actual), `POST /admin/etl/run` (trigger ejecución manual con validación de no ejecución concurrente), `GET /admin/etl/executions/{id}/logs` (logs detallados).  | Backend Lead                   |
| **Streaming logs SSE/polling**      | Implementar Server-Sent Events o endpoint de polling para transmitir logs en tiempo real durante ejecución ETL a la UI.                                                                                     | Backend Lead + QA/DevOps Lead  |
| **Script ETL extractores**          | Desarrollar extractores en `/etl/src/extractors/` para fuentes: IDRD (API/scraping), Portales Distritales, con manejo de errores y rate limiting.                                                           | Data/ETL Lead                  |
| **Transformers y loaders ETL**      | Implementar transformación de datos (normalización de campos, mapeo de tipos, geocodificación) y carga en PostgreSQL con detección de duplicados (título + fecha + ubicación).                              | Data/ETL Lead                  |
| **Logging integral ETL**            | Sistema de logging con niveles (INFO, WARNING, ERROR) que registre cada etapa del proceso, errores específicos y contadores de éxito/fallo.                                                                 | Data/ETL Lead                  |
| **Dockerfile y Compose ETL**        | Crear Dockerfile específico para servicio ETL con dependencias aisladas, configuración en docker-compose.yml con volúmenes para logs y acceso a BD.                                                         | Data/ETL Lead + QA/DevOps Lead |

### Frontend

| Tarea                             | Descripción                                                                                                                                                        | Responsable    |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- |
| **Página `/admin/dashboard`**     | Dashboard responsivo con layout de grid, cards de métricas (usuarios, actividades), gráficos Recharts (pastel por localidad, barras por tipo), y listas top 10.    | Frontend Lead  |
| **Componentes dashboard**         | Crear `MetricCard` (valor + cambio/trend), `TrendIndicator` (flecha arriba/abajo), `ChartContainer` (wrapper para gráficos con títulos/leyendas).                  | Frontend Lead  |
| **Hooks dashboard**               | Implementar `useAdminDashboard` con React Query, manejo de cache (5 min stale time), refetch manual y estados de error/loading.                                    | Frontend Lead  |
| **Página `/admin/usuarios`**      | Tabla con columnas (nombre, email, rol, estado, fecha registro, acciones), filtros (rol, estado, búsqueda), paginación y ordenamiento.                             | Frontend Lead  |
| **Acciones gestión usuarios**     | Modales/dropdowns para cambiar rol y estado con confirmación, hooks `useUpdateUserRole` y `useUpdateUserStatus`, feedback visual (toast), invalidación de queries. | Frontend Lead  |
| **Página `/admin/etl`**           | Interfaz con estado actual (running/idle), botón trigger manual, barra de progreso, streaming de logs en tiempo real (autoscroll), historial de ejecuciones.       | Frontend Lead  |
| **Componente `LogViewer`**        | Visor de logs con autoscroll, colores por nivel (error rojo, warning amarillo, info gris), filtros por nivel, opción de descarga.                                  | Frontend Lead  |
| **Página `/admin/validacion`**    | Lista de actividades con estado `pendiente_validacion`, cards expandibles con detalles, acciones: aprobar, editar y aprobar, rechazar con motivo.                  | Frontend Lead  |
| **Formularios validación rápida** | Form inline para editar campos antes de aprobar, validaciones dinámicas, hooks `useApproveActivity` y `useRejectActivity` con feedback.                            | Frontend Lead  |
| **Hooks ETL**                     | Implementar `useEtlStatus`, `useRunEtl`, `useEtlLogs` (con polling o SSE), `usePendingActivities` con React Query.                                                 | Frontend Lead  |
| **Tests dashboard y ETL**         | Unit tests de componentes y hooks, E2E con Playwright del flujo completo: ver dashboard, gestionar usuarios, ejecutar ETL, validar actividades.                    | QA/DevOps Lead |

### Coordinación

| Tarea                                      | Responsable                   |
| ------------------------------------------ | ----------------------------- |
| Configurar caché dashboard                 | Backend Lead + QA/DevOps Lead |
| Coordinación con fuentes de datos externas | PM                            |
| Seguimiento KPIs y comunicación del sprint | PM                            |

---

## Sprint 5 (Semana 3) · Testing Final + Optimización + Deployment

### Backend

| Tarea                                | Descripción                                                                                                                              | Responsable                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **Validación índices BD**            | Auditar índices existentes, agregar índices faltantes en queries frecuentes, analizar EXPLAIN de queries lentas y optimizar.             | Backend Lead                  |
| **Rate limiting endpoints públicos** | Implementar rate limiting con Redis en endpoints públicos (/actividades, /recomendaciones) para prevenir abuso: 100 req/min por IP.      | Backend Lead + QA/DevOps Lead |
| **Performance testing API**          | Ejecutar pruebas de carga con Locust/K6 simulando 200 usuarios concurrentes, identificar bottlenecks y optimizar queries/cache.          | QA/DevOps Lead + Backend Lead |
| **Code review y refactors**          | Revisión de código backend/frontend, refactoring de duplicación, aplicación de principios SOLID, mejora de legibilidad y mantenibilidad. | Backend Lead + Frontend Lead  |
| **Cobertura tests backend (>80%)**   | Completar tests unitarios e integración para alcanzar mínimo 80% coverage, usando pytest y coverage.py.                                  | QA/DevOps Lead                |
| **Seguridad SAST**                   | Ejecutar Bandit/Semgrep para detectar vulnerabilidades en código Python, corregir issues críticos y altos.                               | QA/DevOps Lead + Backend Lead |
| **Dependency checks**                | Auditar dependencias con safety/pip-audit, actualizar paquetes con vulnerabilidades conocidas.                                           | QA/DevOps Lead                |
| **Actualización doc API**            | Actualizar documentación OpenAPI/Swagger con todos los endpoints, esquemas, ejemplos y descripciones completas.                          | Backend Lead                  |

### Frontend

| Tarea                                   | Descripción                                                                                                                                 | Responsable                    |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **Code splitting y lazy loading**       | Implementar lazy loading de rutas con TanStack Router, code splitting de componentes pesados (gráficos, mapas) para reducir bundle inicial. | Frontend Lead                  |
| **Lazy loading imágenes**               | Usar lazy loading nativo en imágenes, placeholders blur/skeleton, optimización de tamaños con srcset.                                       | Frontend Lead                  |
| **Auditoría accesibilidad WCAG 2.1 AA** | Revisar roles ARIA, navegación por teclado, focus management, contrastes de color (mínimo 4.5:1), textos alternativos en imágenes.          | QA/DevOps Lead + Frontend Lead |
| **Testing cross-browser**               | Probar en Chrome, Firefox, Safari, Edge (últimas 2 versiones) verificando funcionalidad completa y estilos consistentes.                    | QA/DevOps Lead                 |
| **Testing responsive**                  | Verificar diseño y funcionalidad en desktop (1920px, 1366px), tablet (768px, 1024px) y mobile (375px, 414px).                               | QA/DevOps Lead                 |
| **Lighthouse audits**                   | Ejecutar audits de Lighthouse, alcanzar targets: Performance >90 desktop/>80 mobile, Accessibility >95, Best Practices >90, SEO >85.        | QA/DevOps Lead + Frontend Lead |
| **Cobertura tests frontend (>70%)**     | Completar tests unitarios con Vitest + Testing Library para alcanzar mínimo 70% coverage en componentes y hooks.                            | QA/DevOps Lead                 |
| **Tests E2E completos**                 | Suite completa de tests E2E con Playwright cubriendo flujos principales: auth, búsqueda, favoritos, recomendaciones, admin CRUD.            | QA/DevOps Lead                 |
| **Smoke tests pre-deploy**              | Suite mínima de tests críticos que se ejecuten antes de cada deploy para validar funcionalidad básica.                                      | QA/DevOps Lead                 |
| **Optimización bundle**                 | Analizar bundle con tools de Vite, eliminar dependencias no usadas, tree shaking, minificación óptima.                                      | Frontend Lead                  |
| **Actualización doc frontend**          | Documentar estructura de componentes, guía de estilos, convenciones de código, setup local en README.                                       | Frontend Lead                  |

### DevOps & Deploy

| Tarea                           | Descripción                                                                                                                       | Responsable         |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| **CI/CD GitHub Actions**        | Pipeline completo: lint, tests unitarios/E2E, build, security scans, deploy automático a staging/producción con aprobaciones.     | QA/DevOps Lead      |
| **Setup servidores producción** | Configurar servidores, Nginx reverse proxy, SSL/TLS, firewalls, acceso SSH restringido, variables de entorno seguras.             | QA/DevOps Lead + PM |
| **Monitoreo y logging**         | Implementar monitoreo con Prometheus/Grafana o similar, logging centralizado, alertas para errores críticos y caída de servicios. | QA/DevOps Lead      |
| **Backups automatizados**       | Configurar backups automáticos diarios de PostgreSQL con retención de 30 días, verificación de restauración.                      | QA/DevOps Lead      |
| **Load testing (200 usuarios)** | Ejecutar pruebas de carga simulando 200 usuarios concurrentes durante 15 minutos, validar estabilidad y tiempos de respuesta.     | QA/DevOps Lead      |
| **Deploy final a producción**   | Despliegue coordinado de backend + frontend + BD a producción, verificación post-deploy, rollback plan disponible.                | QA/DevOps Lead + PM |

### Documentación y Cierre

| Tarea                                                        | Responsable                       |
| ------------------------------------------------------------ | --------------------------------- |
| Actualizar README completo (setup, arquitectura, deployment) | PM + Backend Lead + Frontend Lead |
| Preparar assets para demo final                              | Frontend Lead                     |
| Video demo (5-10 min) y presentación final                   | PM                                |
| Retrospectiva de equipo                                      | PM                                |

---

## Acciones Transversales (Durante los 3 sprints)

| Tarea                                             | Responsable                  |
| ------------------------------------------------- | ---------------------------- |
| Gestión de riesgos, dependencias y stakeholders   | PM                           |
| Mantenimiento de backlog y refinamiento continuo  | PM                           |
| Soporte de QA a desarrollo continuo (bug triage)  | QA/DevOps Lead               |
| Comunicación interna (dailies, sincronizaciones)  | PM                           |
| Actualización periódica de métricas y reportes    | PM                           |
| Revisión de pull requests y code reviews cruzadas | Backend Lead + Frontend Lead |
| Contract testing (OpenAPI, DTOs, mocks)           | Backend Lead + Frontend Lead |
