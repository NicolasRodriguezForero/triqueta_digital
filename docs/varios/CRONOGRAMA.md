# Cronograma del Proyecto - Triqueta Digital

**Período:** 22 de Septiembre - 22 de Noviembre de 2025 (61 días calendario)

---

## 📅 Resumen Ejecutivo

| Métrica            | Valor                                  |
| ------------------ | -------------------------------------- |
| **Duración Total** | 9 semanas (61 días)                    |
| **Fecha Inicio**   | 22 de Septiembre de 2025               |
| **Fecha Fin**      | 22 de Noviembre de 2025                |
| **Entrega MVP**    | 2 de Noviembre de 2025 (Semana 6)      |
| **Equipo**         | 5 personas                             |
| **Metodología**    | Scrum adaptado con sprints de 1 semana |

---

## 👥 Equipo y Roles

| Rol                            | Responsabilidad Principal                       | Dedicación           |
| ------------------------------ | ----------------------------------------------- | -------------------- |
| **Tech Lead + Backend Senior** | Arquitectura, Auth, Activities, Recommendations | 100% Backend         |
| **Backend Developer + IA**     | Favoritos, ETL, Admin, Algoritmo IA             | 100% Backend         |
| **Frontend Lead**              | Arquitectura React, Setup UI, Componentes Core  | 100% Frontend        |
| **Frontend Developer + UX**    | Componentes, Responsive, Accesibilidad          | 100% Frontend        |
| **DevOps + QA + Full-Stack**   | Docker, CI/CD, Tests, Deployment                | 60% DevOps + 40% Dev |

---

## 🎯 Hitos Principales

| Fecha           | Hito                      | Descripción                         |
| --------------- | ------------------------- | ----------------------------------- |
| **28 Sep 2025** | ✅ Planificación Completa | SRS, arquitectura, setup inicial    |
| **5 Oct 2025**  | ✅ Infraestructura Lista  | Docker, DB, CI/CD básico            |
| **12 Oct 2025** | ✅ Autenticación Completa | OAuth2 + JWT funcional              |
| **19 Oct 2025** | ✅ Módulo Actividades     | CRUD + búsqueda + filtros           |
| **26 Oct 2025** | ✅ Favoritos + IA         | Sistema completo de recomendaciones |
| **2 Nov 2025**  | 🚀 **MVP LISTO**          | **Entrega del MVP funcional**       |
| **9 Nov 2025**  | ✅ Admin Dashboard        | Panel completo con métricas         |
| **16 Nov 2025** | ✅ ETL + Testing Final    | Pipeline completo + tests E2E       |
| **22 Nov 2025** | 🎉 **ENTREGA FINAL**      | **Proyecto completo deployado**     |

---

## 📆 Cronograma Detallado por Semanas

### **Semana 0: Planificación y Diseño Inicial**

**📅 22 - 28 de Septiembre de 2025** (7 días)

#### Objetivos:

- Definición de alcance y requisitos
- Diseño de arquitectura del sistema
- Setup de repositorios y herramientas

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Definir arquitectura SOA modular
- [ ] Diseñar modelo de datos PostgreSQL
- [ ] Crear estructura de proyecto backend (FastAPI)
- [ ] Definir convenciones de código (PEP 8, type hints)
- [ ] Setup repositorio Git + branching strategy

**Backend Developer + IA:**

- [ ] Investigar fuentes de datos (IDRD, APIs públicas)
- [ ] Diseñar algoritmo de recomendaciones MVP
- [ ] Definir esquema de ETL
- [ ] Crear especificación de endpoints API

**Frontend Lead:**

- [ ] Definir arquitectura frontend (React + Vite)
- [ ] Crear sistema de diseño con Shadcn UI
- [ ] Setup de Tanstack Router
- [ ] Wireframes de páginas principales

**Frontend Developer + UX:**

- [ ] Diseñar flujo de usuario completo
- [ ] Crear guía de accesibilidad (WCAG 2.1)
- [ ] Mockups de UI/UX en Figma
- [ ] Definir paleta de colores y tipografía

**DevOps + QA:**

- [ ] Setup de Docker Compose (dev environment)
- [ ] Configurar GitHub Actions (CI básico)
- [ ] Definir estrategia de testing
- [ ] Setup de PostgreSQL + Redis en Docker

#### Entregables:

- ✅ SRS completo (Software Requirements Specification)
- ✅ Diagrama de arquitectura
- ✅ Modelo de datos (ERD)
- ✅ Wireframes y mockups
- ✅ Repositorio configurado
- ✅ Docker Compose funcional

---

### **Semana 1: Setup e Infraestructura**

**📅 29 Sep - 5 Oct de 2025** (7 días)

#### Objetivos:

- Infraestructura base funcional
- Backend y frontend inicializados
- CI/CD básico operativo

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Crear proyecto FastAPI con estructura modular
- [ ] Configurar SQLAlchemy 2.0 (async)
- [ ] Setup de Pydantic schemas
- [ ] Configurar variables de entorno
- [ ] Crear primera migración Alembic (tabla usuarios)

**Backend Developer + IA:**

- [ ] Setup de Redis para caché
- [ ] Configurar logging y manejo de errores
- [ ] Crear middleware de CORS
- [ ] Setup de Swagger/OpenAPI docs

**Frontend Lead:**

- [ ] Crear proyecto React + Vite
- [ ] Configurar TypeScript estricto
- [ ] Setup de Tanstack Router
- [ ] Configurar Axios con interceptors
- [ ] Integrar Shadcn UI

**Frontend Developer + UX:**

- [ ] Setup de TailwindCSS
- [ ] Crear componentes base (Button, Input, Card)
- [ ] Configurar ESLint + Prettier
- [ ] Crear layout principal (Header, Footer)

**DevOps + QA:**

- [ ] Finalizar Docker Compose (backend, frontend, db, redis)
- [ ] Configurar GitHub Actions (lint + build)
- [ ] Setup de base de datos de testing
- [ ] Configurar pytest para backend

#### Entregables:

- ✅ Backend API corriendo en `http://localhost:8000`
- ✅ Frontend corriendo en `http://localhost:3000`
- ✅ PostgreSQL + Redis funcionales
- ✅ CI ejecutando lint y build
- ✅ Documentación de setup en README.md

---

### **Sprint 1: Autenticación y Usuarios**

**📅 6 - 12 Oct de 2025** (7 días)

#### Objetivos:

- Sistema completo de autenticación OAuth2 + JWT
- Gestión de perfil de usuario
- Tests unitarios de autenticación

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Implementar modelo User (SQLAlchemy)
- [ ] Implementar modelo UserProfile
- [ ] Implementar modelo RefreshToken
- [ ] Crear servicio de autenticación (auth_service.py)
- [ ] Implementar hash de passwords (bcrypt)
- [ ] Generar JWT con RS256
- [ ] Endpoints: POST /auth/register, POST /auth/login
- [ ] Endpoints: POST /auth/refresh, POST /auth/logout
- [ ] Escribir 12+ tests unitarios

**Backend Developer + IA:**

- [ ] Implementar rate limiting en endpoints de auth
- [ ] Crear validaciones de password (Pydantic)
- [ ] Implementar revocación de tokens
- [ ] Endpoint: GET /users/me
- [ ] Endpoint: PATCH /users/me (actualizar perfil)
- [ ] Escribir 8+ tests unitarios

**Frontend Lead:**

- [ ] Crear contexto de autenticación (AuthContext)
- [ ] Implementar página de registro (/register)
- [ ] Implementar página de login (/login)
- [ ] Configurar interceptor de Axios para JWT
- [ ] Implementar refresh token automático
- [ ] Protected routes con Tanstack Router

**Frontend Developer + UX:**

- [ ] Diseñar formularios de registro y login
- [ ] Implementar validación de formularios
- [ ] Crear página de perfil (/profile)
- [ ] Implementar edición de perfil
- [ ] Feedback visual (loading, success, error)
- [ ] Validación de accesibilidad en forms

**DevOps + QA:**

- [ ] Tests de integración de autenticación
- [ ] Configurar variables de entorno para JWT
- [ ] Generar claves RSA para JWT en producción
- [ ] Tests E2E: registro y login (Playwright)

#### Entregables:

- ✅ RF-001 a RF-005 implementados
- ✅ 20+ tests unitarios pasando
- ✅ Frontend con autenticación completa
- ✅ Documentación de API en Swagger

---

### **Sprint 2: Módulo de Actividades - Parte 1**

**📅 13 - 19 Oct de 2025** (7 días)

#### Objetivos:

- CRUD completo de actividades (admin)
- Listado con filtros y paginación
- Búsqueda full-text

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Crear modelo Activity (SQLAlchemy)
- [ ] Crear índices optimizados (localidad, tipo, fecha, etiquetas)
- [ ] Implementar full-text search (PostgreSQL)
- [ ] Crear servicio activity_service.py
- [ ] Endpoint: POST /actividades (admin only)
- [ ] Endpoint: PUT /actividades/{id} (admin only)
- [ ] Endpoint: DELETE /actividades/{id} (soft delete, admin)
- [ ] Escribir 15+ tests unitarios

**Backend Developer + IA:**

- [ ] Endpoint: GET /actividades (con filtros y paginación)
- [ ] Endpoint: GET /actividades/{id}
- [ ] Endpoint: GET /actividades/search (búsqueda)
- [ ] Implementar registro de vistas (popularidad)
- [ ] Validaciones de datos (Pydantic schemas)
- [ ] Escribir 10+ tests unitarios

**Frontend Lead:**

- [ ] Crear servicio API activities.ts
- [ ] Implementar hooks de React Query (useActivities, useActivity)
- [ ] Crear componente ActivityCard
- [ ] Crear página /actividades (listado)
- [ ] Implementar paginación
- [ ] Crear SearchBar component

**Frontend Developer + UX:**

- [ ] Crear componente ActivityFilters (Sheet)
- [ ] Crear página /actividades/$id (detalle)
- [ ] Diseño responsive del listado (grid)
- [ ] Implementar skeleton loaders
- [ ] Crear badges para etiquetas
- [ ] Optimizar lazy loading de imágenes

**DevOps + QA:**

- [ ] Tests de integración de actividades
- [ ] Performance testing de búsqueda
- [ ] Validar índices de PostgreSQL
- [ ] Tests E2E: exploración de actividades

#### Entregables:

- ✅ RF-006, RF-007, RF-008 implementados
- ✅ 25+ tests unitarios pasando
- ✅ Frontend con exploración funcional
- ✅ Búsqueda optimizada (<2s P90)

---

### **Sprint 3: Módulo de Actividades - Parte 2 + Admin**

**📅 20 - 26 Oct de 2025** (7 días)

#### Objetivos:

- CRUD de actividades desde frontend (admin)
- Importación CSV/JSON
- Panel de administración básico

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Implementar servicio activity_import_service.py
- [ ] Parser de CSV con validación
- [ ] Parser de JSON con validación
- [ ] Detección de duplicados
- [ ] Endpoint: POST /admin/actividades/import
- [ ] Escribir 8+ tests de importación

**Backend Developer + IA:**

- [ ] Endpoint: GET /admin/actividades (sin filtros públicos)
- [ ] Endpoint: POST /admin/actividades/{id}/aprobar
- [ ] Endpoint: POST /admin/actividades/{id}/rechazar
- [ ] Implementar estados: activa, pendiente_validacion, rechazada
- [ ] Rate limiting en endpoints admin

**Frontend Lead:**

- [ ] Crear página /admin/actividades
- [ ] Implementar ActivityForm (crear/editar)
- [ ] Hooks: useCreateActivity, useUpdateActivity, useDeleteActivity
- [ ] Implementar dialogs de confirmación
- [ ] Tabla de administración con acciones

**Frontend Developer + UX:**

- [ ] Formulario completo de actividad (todos los campos)
- [ ] Validación de formularios
- [ ] Upload de archivos CSV/JSON (importación)
- [ ] Feedback de importación (resumen de errores)
- [ ] Enlace "Administración" en Navbar (solo admins)

**DevOps + QA:**

- [ ] Tests de importación CSV/JSON
- [ ] Validar permisos de admin en endpoints
- [ ] Tests E2E: CRUD de actividades (admin)
- [ ] Performance testing con 1000+ actividades

#### Entregables:

- ✅ RF-009, RF-010 implementados
- ✅ Panel de administración funcional
- ✅ Importación CSV/JSON validada
- ✅ 15+ tests adicionales

---

### **Sprint 4: Favoritos + Recomendaciones IA**

**📅 27 Oct - 2 Nov de 2025** (7 días)

#### Objetivos:

- Sistema completo de favoritos
- Algoritmo de recomendaciones IA
- Optimización con Redis

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Crear modelo Favorite (SQLAlchemy)
- [ ] Endpoint: POST /favoritos (guardar)
- [ ] Endpoint: GET /favoritos (listar propios)
- [ ] Endpoint: DELETE /favoritos/{actividad_id}
- [ ] Actualizar popularidad al guardar/eliminar
- [ ] Escribir 10+ tests de favoritos

**Backend Developer + IA:**

- [ ] Implementar recommendation_service.py
- [ ] Algoritmo híbrido (popularidad + etiquetas + localidad)
- [ ] Endpoint: GET /recomendaciones
- [ ] Generar explicaciones de recomendaciones
- [ ] Implementar caché de recomendaciones en Redis
- [ ] Job para recalcular popularidad_normalizada
- [ ] Escribir 12+ tests de IA

**Frontend Lead:**

- [ ] Crear servicio favorites.ts
- [ ] Hooks: useFavorites, useAddFavorite, useRemoveFavorite
- [ ] Componente FavoriteButton
- [ ] Página /favoritos (listado)
- [ ] Integrar FavoriteButton en ActivityCard

**Frontend Developer + UX:**

- [ ] Crear servicio recommendations.ts
- [ ] Hook: useRecommendations
- [ ] Página /recomendaciones
- [ ] Mostrar explicaciones de recomendaciones
- [ ] Diseño de cards de recomendaciones
- [ ] Animaciones y transiciones

**DevOps + QA:**

- [ ] Tests de integración favoritos + recomendaciones
- [ ] Validar performance de algoritmo IA (<1s)
- [ ] Tests de caché Redis
- [ ] Tests E2E: flujo completo de favoritos
- [ ] **Deploy del MVP a staging**

#### Entregables:

- ✅ RF-011, RF-012, RF-013, RF-014, RF-015 implementados
- ✅ 🚀 **MVP COMPLETO Y FUNCIONAL**
- ✅ 22+ tests adicionales
- ✅ MVP deployado en ambiente staging

---

### **Sprint 5: Dashboard de Administración**

**📅 3 - 9 Nov de 2025** (7 días)

#### Objetivos:

- Dashboard con métricas clave
- Gestión avanzada de usuarios (admin)
- Visualizaciones y reportes

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Endpoint: GET /admin/dashboard (métricas)
- [ ] Queries optimizadas para métricas
- [ ] Métricas: usuarios totales, activos, nuevos
- [ ] Métricas: actividades por localidad/tipo
- [ ] Implementar caché de 5 minutos para dashboard

**Backend Developer + IA:**

- [ ] Endpoint: GET /admin/usuarios (listado)
- [ ] Endpoint: GET /admin/usuarios/{id}
- [ ] Endpoint: PATCH /admin/usuarios/{id}/rol
- [ ] Endpoint: PATCH /admin/usuarios/{id}/estado
- [ ] Top 10 actividades más populares
- [ ] Top 10 etiquetas más usadas

**Frontend Lead:**

- [ ] Crear página /admin/dashboard
- [ ] Integrar librería de gráficos (Recharts o similar)
- [ ] Gráfico de torta: actividades por localidad
- [ ] Gráfico de barras: actividades por tipo
- [ ] Cards con métricas clave

**Frontend Developer + UX:**

- [ ] Crear página /admin/usuarios
- [ ] Tabla de usuarios con filtros
- [ ] Dialogs para cambiar rol/estado
- [ ] Lista de top actividades populares
- [ ] Lista de top etiquetas
- [ ] Diseño responsive del dashboard

**DevOps + QA:**

- [ ] Tests de performance de queries de dashboard
- [ ] Validar caché de métricas
- [ ] Tests E2E: dashboard completo
- [ ] Monitoreo de performance con Prometheus (opcional)

#### Entregables:

- ✅ RF-021, RF-022 implementados
- ✅ Dashboard completo y funcional
- ✅ Gestión de usuarios implementada
- ✅ 10+ tests adicionales

---

### **Sprint 6: ETL + Importación Automatizada**

**📅 10 - 16 Nov de 2025** (7 días)

#### Objetivos:

- Pipeline ETL completo en Docker separado
- Gestión de procesos ETL desde admin
- Validación de actividades importadas

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Crear modelo ETLExecution
- [ ] Endpoint: GET /admin/etl/status
- [ ] Endpoint: POST /admin/etl/run (ejecutar manual)
- [ ] Endpoint: GET /admin/etl/executions/{id}/logs
- [ ] Implementar SSE o polling para logs en tiempo real

**Backend Developer + IA:**

- [ ] Crear script ETL en /etl/src/
- [ ] Extractor: API IDRD
- [ ] Extractor: Portales Distritales (CSV/JSON)
- [ ] Transformer: normalización de datos
- [ ] Loader: inserción en PostgreSQL
- [ ] Detección de duplicados
- [ ] Logging completo del proceso

**Frontend Lead:**

- [ ] Crear página /admin/etl
- [ ] Visualizar estado de última ejecución
- [ ] Botón para ejecutar ETL manual
- [ ] Visualizar logs en tiempo real
- [ ] Tabla de ejecuciones históricas

**Frontend Developer + UX:**

- [ ] Página /admin/validacion
- [ ] Listado de actividades pendientes de validación
- [ ] Acciones: aprobar, editar+aprobar, rechazar
- [ ] Filtros por fuente de datos
- [ ] Resumen de importación (exitosos, errores, duplicados)

**DevOps + QA:**

- [ ] Crear Dockerfile para ETL
- [ ] Configurar Docker Compose para ETL
- [ ] Tests de integración del pipeline completo
- [ ] Validar manejo de errores en ETL
- [ ] Tests E2E: ejecución y validación

#### Entregables:

- ✅ RF-016, RF-017, RF-018 implementados
- ✅ Pipeline ETL funcional
- ✅ Docker separado para ETL
- ✅ 12+ tests de ETL

---

### **Sprint 7: Testing Final y Optimización**

**📅 17 - 22 Nov de 2025** (6 días)

#### Objetivos:

- Testing completo E2E
- Optimización de performance
- Deployment a producción
- Documentación final

#### Tareas por Rol:

**Tech Lead + Backend Senior:**

- [ ] Code review completo del backend
- [ ] Refactoring y optimizaciones
- [ ] Validar todos los índices de BD
- [ ] Implementar rate limiting en todos los endpoints
- [ ] Actualizar documentación de API

**Backend Developer + IA:**

- [ ] Performance testing completo
- [ ] Optimizar queries lentas
- [ ] Implementar caché donde aplique
- [ ] Validar cobertura de tests >80%
- [ ] Generar reporte de coverage

**Frontend Lead:**

- [ ] Code review completo del frontend
- [ ] Optimizar bundle size (code splitting)
- [ ] Implementar lazy loading
- [ ] Validar accesibilidad (Lighthouse >95)
- [ ] Optimizar Core Web Vitals

**Frontend Developer + UX:**

- [ ] Testing de accesibilidad completo (WCAG 2.1 AA)
- [ ] Testing en múltiples navegadores
- [ ] Testing en múltiples dispositivos
- [ ] Corrección de bugs de UI/UX
- [ ] Validar cobertura de tests >70%

**DevOps + QA:**

- [ ] **Suite completa de tests E2E (Playwright)**
- [ ] Load testing (200 usuarios concurrentes)
- [ ] Security scan (SAST con Bandit/Semgrep)
- [ ] Dependency check
- [ ] **Configurar CI/CD completo**
- [ ] **Setup de servidor de producción**
- [ ] **Deploy a producción**
- [ ] Configurar monitoreo y alertas
- [ ] Backups automáticos de BD

#### Tareas Finales (Todo el Equipo):

- [ ] Actualizar README.md con instrucciones completas
- [ ] Crear DEPLOYMENT.md
- [ ] Crear CONTRIBUTING.md
- [ ] Video demo del proyecto (5-10 min)
- [ ] Presentación final del proyecto
- [ ] Post-mortem y retrospectiva

#### Entregables:

- ✅ **PROYECTO COMPLETO DEPLOYADO**
- ✅ Cobertura de tests: >80% backend, >70% frontend
- ✅ Lighthouse Performance: >90 (desktop), >80 (mobile)
- ✅ Lighthouse Accessibility: >95
- ✅ Documentación completa
- ✅ Video demo
- ✅ 🎉 **ENTREGA FINAL: 22 de Noviembre de 2025**

---

## 📊 Distribución de Esfuerzo por Fase

| Fase          | Duración | % Proyecto | Actividad Principal     |
| ------------- | -------- | ---------- | ----------------------- |
| Planificación | 7 días   | 11%        | Diseño y setup          |
| Setup         | 7 días   | 11%        | Infraestructura         |
| Sprint 1      | 7 días   | 11%        | Autenticación           |
| Sprint 2      | 7 días   | 11%        | Actividades (backend)   |
| Sprint 3      | 7 días   | 11%        | Actividades (admin)     |
| Sprint 4      | 7 días   | 11%        | **MVP: Favoritos + IA** |
| Sprint 5      | 7 días   | 11%        | Dashboard admin         |
| Sprint 6      | 7 días   | 11%        | ETL completo            |
| Sprint 7      | 6 días   | 12%        | Testing + Deploy        |

---

## 🎯 Métricas de Éxito del Proyecto

Al finalizar el proyecto (22 de noviembre), se deben cumplir:

### Funcionalidades

- ✅ RF-001 a RF-018: Implementados y testeados
- ✅ ETL funcional con al menos 2 fuentes de datos
- ✅ MVP deployado y accesible públicamente

### Calidad

- ✅ Cobertura de tests backend: >80%
- ✅ Cobertura de tests frontend: >70%
- ✅ 0 vulnerabilidades críticas (SAST)
- ✅ Lighthouse Accessibility: >95
- ✅ Lighthouse Performance: >90 (desktop), >80 (mobile)

### Performance

- ✅ Tiempo de respuesta API P90: <2s
- ✅ Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
- ✅ Load testing exitoso con 200 usuarios concurrentes

### Documentación

- ✅ SRS completo
- ✅ README.md con setup completo
- ✅ API documentada en Swagger
- ✅ DEPLOYMENT.md
- ✅ Video demo del proyecto

### Datos

- ✅ Base de datos con 150+ actividades
- ✅ Sistema de recomendaciones funcional
- ✅ ETL ejecutado al menos 2 veces exitosamente

---

## ⚠️ Riesgos y Mitigaciones

| Riesgo                           | Probabilidad | Impacto | Mitigación                                     |
| -------------------------------- | ------------ | ------- | ---------------------------------------------- |
| **Retraso en autenticación**     | Media        | Alto    | Priorizar en Sprint 1, pair programming        |
| **APIs externas no disponibles** | Alta         | Medio   | Preparar datos mock, CSV manual                |
| **Performance de búsqueda**      | Media        | Alto    | Índices desde el inicio, testing temprano      |
| **Complejidad del algoritmo IA** | Media        | Medio   | Algoritmo MVP simple, iterar después           |
| **Problemas de deployment**      | Media        | Alto    | Preparar Docker desde semana 1, CI/CD temprano |
| **Testing insuficiente**         | Alta         | Alto    | Definition of Done incluye tests, QA continuo  |
| **Scope creep**                  | Alta         | Alto    | Priorización estricta, focus en MVP            |

---

## 📈 Indicadores de Progreso Semanal

Cada semana se evaluará:

1. **% Completitud de tareas** (target: >90%)
2. **Tests pasando** (target: 100%)
3. **Code coverage** (target: incremental hasta >80%/>70%)
4. **Bugs críticos** (target: 0)
5. **Deploy exitoso** (target: sí/no)

---

## 🚀 Estrategia de Deployment

### Ambientes

| Ambiente        | Uso                      | URL                  | Deploy                      |
| --------------- | ------------------------ | -------------------- | --------------------------- |
| **Development** | Local con Docker Compose | localhost            | Manual                      |
| **Staging**     | Testing MVP (Sprint 4)   | staging.triqueta.com | Automático (develop branch) |
| **Production**  | Release final            | triqueta.com         | Manual (main branch)        |

### Pipeline CI/CD

```
Git Push → Lint → Test → Build → Security Scan → Deploy
```

- **Develop branch** → Auto-deploy a Staging
- **Main branch** → Manual deploy a Production (con aprobación)

---

## 📝 Notas Finales

### Días de Alta Intensidad

- **Sprint 1-4** (6-26 Oct): Desarrollo intensivo del MVP
- **Última semana** (17-22 Nov): Testing y deployment

### Días de Menor Presión

- **Semana 0** (22-28 Sep): Planificación sin código
- **Sprints 5-6** (3-16 Nov): Post-MVP, menor presión

### Recomendaciones

1. **Daily standups** de 15 min cada mañana
2. **Code reviews** obligatorios en cada PR
3. **Retrospectiva** al final de cada sprint
4. **Testing continuo** desde Sprint 1
5. **Documentar mientras desarrollas**, no al final

---

**Última actualización:** 21 de Octubre de 2025  
**Versión:** 1.0  
**Estado:** ✅ Aprobado para ejecución

---

## 🎓 Equipo Triqueta Digital

**Proyecto:** Diseño Creativo - 8vo Semestre  
**Universidad:** Universidad Sergio Arboleda  
**Período:** Septiembre - Noviembre 2025

---

**¡Éxito en el proyecto! 🚀**
