# Documentación Técnica - Triqueta Digital

## 📋 Software Requirements Specification (SRS)

Documentación completa de requisitos según **ISO/IEC/IEEE 29148:2018** para el proyecto Triqueta Digital.

---

## 📚 Índice de Documentos

### 1. Documento Principal
**[SRS.md](./SRS.md)** - Software Requirements Specification completo
- Introducción y alcance del proyecto
- Descripción general del sistema
- Resumen de requisitos funcionales y no funcionales
- Arquitectura de alto nivel
- Restricciones y apéndices

### 2. Requisitos Funcionales Detallados
**[SRS_Requisitos_Funcionales.md](./SRS_Requisitos_Funcionales.md)**
- **RF-001 a RF-005:** Autenticación y gestión de usuarios
- **RF-006 a RF-010:** Módulo de actividades
- **RF-011 a RF-013:** Módulo de favoritos
- **RF-014 a RF-015:** Módulo de recomendaciones (IA)
- **RF-016 a RF-018:** Gestión de ingesta (ETL)
- **RF-019 a RF-020:** Dispositivos IoT
- **RF-021 a RF-022:** Administración

### 3. Requisitos No Funcionales Detallados
**[SRS_Requisitos_No_Funcionales.md](./SRS_Requisitos_No_Funcionales.md)**
- **RNF-001 a RNF-003:** Usabilidad y accesibilidad
- **RNF-004 a RNF-007:** Eficiencia y rendimiento
- **RNF-008 a RNF-010:** Compatibilidad
- **RNF-011 a RNF-013:** Fiabilidad
- **RNF-014 a RNF-017:** Seguridad
- **RNF-018 a RNF-020:** Mantenibilidad
- **RNF-021 a RNF-022:** Portabilidad
- **RNF-023 a RNF-024:** Satisfacción del usuario

### 4. Arquitectura y Modelo de Datos
**[SRS_Arquitectura_y_Datos.md](./SRS_Arquitectura_y_Datos.md)**
- Estilo arquitectónico (SOA Modular)
- Stack tecnológico completo
- Estructura de directorios del proyecto
- Modelo de datos PostgreSQL
- Interfaces externas
- Ventajas de PostgreSQL para el proyecto

---

## 🎯 Resumen Ejecutivo

### Proyecto
**Triqueta Digital** - Plataforma digital que conecta actividades culturales, recreativas y deportivas en las localidades de Chapinero, Santa Fe y La Candelaria (Bogotá, Colombia).

### Objetivos Principales
- ✅ Integrar al menos 70% de la oferta cultural y deportiva disponible
- ✅ Proveer recomendaciones personalizadas mediante IA
- ✅ Facilitar participación ciudadana en actividades locales
- ✅ MVP con 200+ usuarios activos mensuales

### Stack Tecnológico

**Frontend:**
```
React 18+ + Vite + TypeScript
TailwindCSS + Shadcn UI + Lucide Icons
Tanstack Router + Tanstack React Query
```

**Backend:**
```
Python 3.11+ + FastAPI
SQLAlchemy 2.0+ (ORM async)
OAuth2 + JWT (RS256)
Redis (caché, rate limiting)
```

**Base de Datos:**
```
PostgreSQL 15+
PostGIS (coordenadas GPS)
```

**Infraestructura:**
```
Docker + Docker Compose
GitHub Actions (CI/CD)
```

### Arquitectura

**SOA Modular** - Monolito modular en FastAPI con servicios internos:
- 🔐 Servicio de Autenticación
- 👤 Servicio de Usuarios
- 🎭 Servicio de Actividades
- 🤖 Servicio de Recomendaciones (IA)
- ⭐ Servicio de Favoritos
- 📊 Servicio de Gestión de Ingesta (ETL)
- 📱 Servicio de Dispositivos IoT
- ⚙️ Servicio de Administración

### ETL Pipeline
Script Docker **separado** del backend para ingesta de datos desde:
- API IDRD
- Portales Distritales
- CSV/JSON

---

## 🚀 Roadmap de Desarrollo

### Fase 1: MVP Core (Semanas 1-4)
- ✅ Autenticación y perfil de usuario
- ✅ Exploración de actividades con filtros
- ✅ Búsqueda full-text
- ✅ Docker Compose setup

### Fase 2: MVP Funcional (Semanas 5-8)
- ✅ CRUD de actividades (admin)
- ✅ Sistema de favoritos
- ✅ Recomendaciones básicas (IA)
- ✅ Optimización de performance

### Fase 3: MVP Completo (Semanas 9-12)
- ✅ Importación manual de actividades
- ✅ Gestión ETL
- ✅ Dashboard administrativo
- ✅ Tests automatizados

### Fase 4: Post-MVP (Futuro)
- 📱 Integración con dispositivo IoT (cubo)
- 🧠 Recomendaciones avanzadas (filtrado colaborativo)
- 🎮 Gamificación
- 🌍 Expansión a otras localidades

---

## 📊 Métricas de Éxito

| Métrica | Objetivo | Método |
|---------|----------|--------|
| **Usuarios registrados** | ≥200 | Analytics, BD |
| **Actividades en catálogo** | ≥150 (70% oferta) | Count BD |
| **CTR recomendaciones** | ≥20% | Event tracking |
| **NPS** | ≥70 | Encuesta |
| **Tiempo respuesta API** | <2s (P90) | APM |
| **Disponibilidad** | ≥99% | Monitoring |
| **Cobertura tests** | >80% backend | Coverage |

---

## 🔒 Cumplimiento Normativo

- ✅ **ISO/IEC/IEEE 29148:2018** - Requirements engineering
- ✅ **ISO/IEC 25010:2023** - Software quality model
- ✅ **OWASP ASVS v5.0 Nivel 2** - Security verification
- ✅ **WCAG 2.1 Level AA** - Accessibility
- ✅ **Ley 1581 de 2012** - Protección de Datos Personales (Colombia)
- ✅ **RFC 6749** - OAuth 2.0
- ✅ **RFC 7519** - JWT

---

## 🎨 Características Principales

### Para Usuarios
1. **Exploración inteligente** - Filtros avanzados por localidad, tipo, fecha, precio
2. **Búsqueda potente** - Full-text search en actividades
3. **Recomendaciones personalizadas** - Basadas en etiquetas y popularidad
4. **Favoritos** - Guarda actividades de interés
5. **Perfil personalizable** - Define intereses, disponibilidad y preferencias

### Para Administradores
1. **CRUD completo** - Gestión de actividades
2. **Importación masiva** - CSV/JSON con validación
3. **Curaduría de datos** - Validación de actividades importadas
4. **Dashboard analytics** - Métricas de uso y engagement
5. **Gestión ETL** - Monitoreo y activación manual de ingesta

### Módulo de IA
**Algoritmo de Recomendación MVP:**
```
Score = Popularidad_Base (0-100)
      + Coincidencias_Etiquetas × 10
      + Bonus_Localidad (5 pts)
      + Bonus_Disponibilidad (3 pts)
```

---

## 🛠️ Decisiones Arquitectónicas Clave

| Decisión | Justificación |
|----------|---------------|
| **SOA Modular (no microservicios)** | Simplicidad operacional, desarrollo rápido en MVP |
| **PostgreSQL** | Relacional + flexible (JSONB, arrays, PostGIS) |
| **FastAPI** | Alto rendimiento, async, type-safe, OpenAPI auto |
| **React + Vite** | Ecosistema maduro, DX excelente, build rápido |
| **Docker Compose** | Portabilidad, consistencia dev-prod |
| **ETL Separado** | Desacoplamiento, ejecuciones independientes |
| **JWT con RS256** | Stateless, escalable, asimétrico seguro |
| **OAuth2 Password Grant** | Estándar, extensible a Social Auth futuro |

---

## 📁 Estructura del Repositorio

```
triqueta-digital/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/      # Routers
│   │   ├── models/      # SQLAlchemy
│   │   ├── schemas/     # Pydantic
│   │   ├── services/    # Business logic
│   │   └── main.py
│   ├── tests/
│   └── Dockerfile
├── frontend/             # React frontend
│   ├── src/
│   │   ├── routes/      # Tanstack Router
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   └── services/    # API client
│   ├── tests/
│   └── Dockerfile
├── etl/                  # ETL pipeline
│   ├── src/
│   │   ├── extractors/
│   │   ├── transformers/
│   │   └── loaders/
│   └── Dockerfile
├── docs/                 # 📚 Esta documentación
├── infra/                # Docker Compose, CI/CD
└── README.md
```

---

## 🔗 Enlaces Útiles

- [Contexto del Proyecto](../Triqueta_Contexto_Proyecto.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## 👥 Equipo y Contacto

**Proyecto:** Diseño Creativo - 8vo Semestre  
**Universidad:** [Universidad Santo Tomás]  
**Fecha:** Octubre 2025

---

## 📄 Licencia

Este proyecto es de carácter académico. Consultar con la entidad académica responsable para uso y distribución.

---

## 🔄 Versión del Documento

**Versión:** 1.0  
**Última actualización:** Octubre 2025  
**Estado:** ✅ Aprobado para desarrollo

---

## 🚦 Próximos Pasos

1. **Setup inicial:**
   - [ ] Crear estructura de directorios
   - [ ] Configurar Docker Compose
   - [ ] Setup backend FastAPI base
   - [ ] Setup frontend React base

2. **Sprint 1 (Semanas 1-2):**
   - [ ] Implementar autenticación (RF-001 a RF-004)
   - [ ] Implementar gestión de perfil (RF-005)
   - [ ] Setup PostgreSQL con migraciones
   - [ ] Tests unitarios de autenticación

3. **Sprint 2 (Semanas 3-4):**
   - [ ] Implementar listado de actividades (RF-006)
   - [ ] Implementar búsqueda (RF-008)
   - [ ] Implementar detalle de actividad (RF-007)
   - [ ] Diseño UI/UX del frontend

4. **Revisión y ajuste:**
   - [ ] Code review
   - [ ] Tests de integración
   - [ ] Ajustes de rendimiento
   - [ ] Documentación de API

---

**¿Preguntas sobre la documentación?**  
Revisa primero los documentos detallados. Si persisten dudas, consulta con el equipo técnico.
