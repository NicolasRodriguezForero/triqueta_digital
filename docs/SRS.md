# Software Requirements Specification (SRS)
## Triqueta Digital - Plataforma de Integración Cultural y Deportiva

**Versión:** 1.0  
**Fecha:** Octubre 2025  
**Estándar de referencia:** ISO/IEC/IEEE 29148:2018

---

## Control de Versiones

| Versión | Fecha | Autor | Descripción |
|---------|-------|-------|-------------|
| 1.0 | Oct 2025 | Equipo Diseño Creativo | Versión inicial del SRS para MVP |

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Descripción General](#2-descripción-general)
3. [Requisitos Funcionales](#3-requisitos-funcionales)
4. [Requisitos No Funcionales](#4-requisitos-no-funcionales)
5. [Arquitectura del Sistema](#5-arquitectura-del-sistema)
6. [Interfaces Externas](#6-interfaces-externas)
7. [Requisitos de Datos](#7-requisitos-de-datos)
8. [Restricciones de Diseño](#8-restricciones-de-diseño)
9. [Apéndices](#9-apéndices)

---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requisitos de software para **Triqueta Digital**, una plataforma digital que conecta actividades culturales, recreativas y deportivas en las localidades de Chapinero, Santa Fe y La Candelaria en Bogotá, Colombia.

El documento está dirigido a:
- Equipo de desarrollo
- Stakeholders del proyecto
- Evaluadores académicos
- Futuros mantenedores del sistema

### 1.2 Alcance del Producto

**Triqueta Digital** es un sistema web que permite:

- **A los ciudadanos:** Descubrir, explorar y recibir recomendaciones personalizadas de actividades culturales, recreativas y deportivas en su localidad.
- **A los administradores:** Gestionar el catálogo de actividades, integrar fuentes públicas y monitorear el uso de la plataforma.
- **Al sistema IoT:** Sincronizar recomendaciones con un dispositivo físico (cubo) vinculado a la cuenta del usuario.

**Objetivos principales:**
- Integrar al menos el 70% de la oferta cultural y deportiva disponible
- Proveer recomendaciones personalizadas mediante IA
- Facilitar la participación ciudadana en actividades locales
- Fortalecer el vínculo comunitario y la apropiación del territorio

**Límites del MVP:**
- Cobertura geográfica: 3 localidades de Bogotá (Chapinero, Santa Fe, La Candelaria)
- Usuarios objetivo inicial: 200+ usuarios activos mensuales
- Actividades objetivo: 70% de la oferta disponible en las localidades
- Dispositivo IoT: Prototipo funcional con sincronización básica

### 1.3 Definiciones, Acrónimos y Abreviaturas

| Término | Definición |
|---------|------------|
| **MVP** | Minimum Viable Product (Producto Mínimo Viable) |
| **SOA** | Service-Oriented Architecture (Arquitectura Orientada a Servicios) |
| **ETL** | Extract, Transform, Load (Extracción, Transformación y Carga) |
| **JWT** | JSON Web Token |
| **CRUD** | Create, Read, Update, Delete |
| **API** | Application Programming Interface |
| **REST** | Representational State Transfer |
| **IoT** | Internet of Things |
| **IDRD** | Instituto Distrital de Recreación y Deporte |
| **WCAG** | Web Content Accessibility Guidelines |
| **OWASP** | Open Web Application Security Project |
| **ASVS** | Application Security Verification Standard |

### 1.4 Referencias

| Estándar/Documento | Descripción |
|--------------------|-------------|
| ISO/IEC/IEEE 29148:2018 | Systems and software engineering — Life cycle processes — Requirements engineering |
| ISO/IEC 25010:2023 | Systems and software Quality Requirements and Evaluation (SQuaRE) |
| OWASP ASVS v5.0 | Application Security Verification Standard |
| ISO/IEC 27001:2022 | Information security management systems |
| WCAG 2.1 Level AA | Web Content Accessibility Guidelines |
| Ley 1581 de 2012 | Protección de Datos Personales (Colombia) |
| RFC 6749 | OAuth 2.0 Authorization Framework |
| RFC 7519 | JSON Web Token (JWT) |

### 1.5 Visión General del Documento

Este documento está organizado según el estándar ISO/IEC/IEEE 29148:2018 y describe:
- Requisitos funcionales del sistema (Sección 3)
- Requisitos no funcionales basados en ISO/IEC 25010:2023 (Sección 4)
- Arquitectura técnica y componentes (Sección 5)
- Interfaces del sistema (Sección 6)
- Modelo y requisitos de datos (Sección 7)

---

## 2. Descripción General

### 2.1 Perspectiva del Producto

Triqueta Digital es un sistema independiente que integra múltiples componentes:

```
┌─────────────────────────────────────────────────────────┐
│                     USUARIOS FINALES                     │
│  (Ciudadanos, Administradores, Dispositivo IoT)         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              FRONTEND WEB APPLICATION                    │
│   React + Vite + TypeScript + TailwindCSS + Shadcn UI  │
│        Tanstack Router + Tanstack React Query           │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS/REST
┌────────────────────▼────────────────────────────────────┐
│            BACKEND API (FastAPI + Python)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Servicio de Autenticación (OAuth2 + JWT)        │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Servicio de Usuarios y Perfiles                 │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Servicio de Actividades (CRUD + Búsqueda)       │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Servicio de Recomendaciones (IA)                │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Servicio de Gestión de Ingesta (ETL Manager)    │  │
│  ├──────────────────────────────────────────────────┤  │
│  │  Servicio de Dispositivos IoT                    │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           BASE DE DATOS POSTGRESQL                       │
│  (Usuarios, Actividades, Interacciones, Dispositivos)   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│              ETL PIPELINE (Script Docker)                 │
│  Extracción → Transformación → Carga                     │
│  (Fuentes: IDRD, Portales Distritales, CSV/JSON)        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     └──→ PostgreSQL
```

**Interacciones principales:**
- Frontend web consume API REST del backend
- Backend modular con servicios internos organizados en un único proyecto FastAPI
- ETL ejecuta como script Docker separado, gestiona ingesta mediante módulo específico
- Dispositivo IoT consume API REST para sincronización

### 2.2 Funciones del Producto

#### Para Usuarios Finales:
1. **Autenticación y perfil:** Registro, login OAuth2+JWT, gestión de perfil
2. **Exploración:** Listado con filtros, búsqueda, vista detallada
3. **Recomendaciones:** Basadas en etiquetas y popularidad
4. **Favoritos:** Guardar y listar actividades

#### Para Administradores:
1. **Gestión de actividades:** CRUD completo, importación manual
2. **Curaduría:** Validación de datos importados
3. **Monitoreo:** Dashboard con métricas

#### Para Sistema IoT:
1. **Sincronización:** Autenticación por token, obtención de recomendaciones top 3-5

### 2.3 Características de Usuarios

| Tipo de Usuario | Descripción | Nivel Técnico | Frecuencia |
|-----------------|-------------|---------------|------------|
| **Ciudadano** | Usuario general que busca actividades | Básico | Semanal/Mensual |
| **Administrador** | Gestiona catálogo y valida datos | Intermedio | Diario/Semanal |
| **Dispositivo IoT** | Cubo físico vinculado a cuenta | N/A | Continuo |

### 2.4 Restricciones

**Tecnológicas:**
- Backend: Python 3.11+ con FastAPI
- Frontend: React 18+ con Vite, TypeScript, TailwindCSS, Shadcn UI, Tanstack Router, Tanstack React Query
- Base de datos: PostgreSQL 15+
- Orquestación: Docker y Docker Compose
- Arquitectura: SOA modular en único proyecto FastAPI

**Regulatorias:**
- Ley 1581 de 2012 (Protección de Datos Personales, Colombia)
- WCAG 2.1 Level AA
- OWASP ASVS v5.0 Nivel 2

**Operacionales:**
- Disponibilidad: 99% uptime
- Tiempo de respuesta: <2s en 90% de requests
- Concurrencia: 200+ usuarios

### 2.5 Suposiciones y Dependencias

**Suposiciones:**
- Usuarios con acceso a internet y navegador moderno
- Fuentes públicas mantienen APIs/datos actualizados
- Dispositivo IoT con conectividad Wi-Fi/BLE

**Dependencias:**
- APIs públicas de IDRD y entidades distritales
- Infraestructura cloud para despliegue
- Librerías open-source

---

## 3. Requisitos Funcionales

**Ver documento detallado:** [`SRS_Requisitos_Funcionales.md`](./SRS_Requisitos_Funcionales.md)

### Resumen de Módulos Funcionales

#### 3.1 Autenticación y Usuarios
- RF-001: Registro de usuario (email/password)
- RF-002: Login con OAuth2 + JWT
- RF-003: Refresh token
- RF-004: Logout
- RF-005: Gestión de perfil

#### 3.2 Actividades
- RF-006: Listar actividades con filtros y paginación
- RF-007: Ver detalle de actividad
- RF-008: Búsqueda full-text
- RF-009: CRUD actividades (admin)
- RF-010: Importación manual CSV/JSON

#### 3.3 Favoritos
- RF-011: Guardar favorito
- RF-012: Listar favoritos
- RF-013: Eliminar favorito

#### 3.4 Recomendaciones (IA)
- RF-014: Obtener recomendaciones personalizadas
- RF-015: Actualizar scoring de popularidad

#### 3.5 Gestión de Ingesta (ETL)
- RF-016: Dashboard de estado ETL
- RF-017: Activar proceso ETL manual
- RF-018: Validar actividades importadas

#### 3.6 Dispositivos IoT (Post-MVP)
- RF-019: Vincular dispositivo
- RF-020: API de sincronización

#### 3.7 Administración
- RF-021: Dashboard con métricas
- RF-022: Gestión de usuarios

---

## 4. Requisitos No Funcionales

**Ver documento detallado:** [`SRS_Requisitos_No_Funcionales.md`](./SRS_Requisitos_No_Funcionales.md)

### Resumen por Categoría ISO/IEC 25010:2023

#### 4.1 Usabilidad
- RNF-001: Accesibilidad WCAG 2.1 Level AA
- RNF-002: Curva de aprendizaje <5 minutos
- RNF-003: Diseño responsive (375px+)

#### 4.2 Eficiencia de Desempeño
- RNF-004: Tiempo de respuesta API <2s (P90)
- RNF-005: Core Web Vitals (LCP <2.5s, FID <100ms, CLS <0.1)
- RNF-006: Capacidad de 200 usuarios concurrentes
- RNF-007: Queries optimizadas con índices

#### 4.3 Compatibilidad
- RNF-008: Navegadores Chrome/Firefox/Safari/Edge 100+
- RNF-009: Dispositivos desktop/móvil/tablet
- RNF-010: API RESTful estándar

#### 4.4 Fiabilidad
- RNF-011: Disponibilidad 99% uptime
- RNF-012: Tolerancia a fallos graceful
- RNF-013: Backups diarios, RTO <4h, RPO <24h

#### 4.5 Seguridad
- RNF-014: OAuth2 + JWT (RS256)
- RNF-015: Protección OWASP Top 10
- RNF-016: Cumplimiento Ley 1581/2012
- RNF-017: Rate limiting

#### 4.6 Mantenibilidad
- RNF-018: Código limpio (PEP 8, ESLint)
- RNF-019: Cobertura de tests >80% backend, >70% frontend
- RNF-020: Documentación completa (Swagger, README)

#### 4.7 Portabilidad
- RNF-021: Docker Compose para todos los servicios
- RNF-022: CI/CD automatizado (GitHub Actions)

#### 4.8 Satisfacción
- RNF-023: NPS >70
- RNF-024: 200+ usuarios registrados en primer mes

---

## 5. Arquitectura del Sistema

**Ver documento detallado:** [`SRS_Arquitectura_y_Datos.md`](./SRS_Arquitectura_y_Datos.md)

### 5.1 Estilo Arquitectónico

**SOA Modular** - Arquitectura orientada a servicios implementada como monolito modular en FastAPI.

### 5.2 Stack Tecnológico

**Frontend:**
- React 18+ + Vite + TypeScript
- TailwindCSS + Shadcn UI + Lucide Icons
- Tanstack Router + Tanstack React Query

**Backend:**
- Python 3.11+ + FastAPI
- SQLAlchemy 2.0+ + Pydantic
- OAuth2 + JWT

**Base de Datos:**
- PostgreSQL 15+
- Redis (caché, rate limiting)

**Infraestructura:**
- Docker + Docker Compose
- GitHub Actions (CI/CD)

### 5.3 Componentes Principales

1. **Frontend Web:** SPA React para usuarios y administradores
2. **Backend API:** FastAPI modular con servicios internos
3. **Base de Datos:** PostgreSQL con PostGIS
4. **ETL Pipeline:** Script Docker separado para ingesta
5. **Dispositivo IoT:** Cubo físico (fase posterior)

---

## 6. Interfaces Externas

### 6.1 API REST

**Base URL:** `/api/v1`

**Autenticación:** Bearer Token (JWT)

**Documentación:** Swagger UI en `/docs`

**Endpoints principales:**
- `/auth/*` - Autenticación
- `/actividades/*` - Gestión de actividades
- `/recomendaciones` - IA/Recomendaciones
- `/favoritos/*` - Favoritos
- `/admin/*` - Administración
- `/iot/*` - Dispositivos IoT

### 6.2 Fuentes de Datos Externas

- **API IDRD:** Actividades deportivas
- **Portales Distritales:** Datos abiertos de Bogotá
- **CSV/JSON:** Importación manual

---

## 7. Requisitos de Datos

### 7.1 Entidades Principales

1. **Usuario:** Información de cuenta y autenticación
2. **Perfil Usuario:** Preferencias y configuración
3. **Actividad:** Eventos culturales/deportivos/recreativos
4. **Favorito:** Relación usuario-actividad
5. **Refresh Token:** Tokens de autenticación
6. **Dispositivo:** Hardware IoT (post-MVP)
7. **ETL Execution:** Logs de procesos ETL

### 7.2 Base de Datos: PostgreSQL

**Ventajas para este proyecto:**
- ✅ Relaciones bien definidas
- ✅ JSONB para campos flexibles
- ✅ Arrays nativos para etiquetas
- ✅ Full-text search integrado
- ✅ PostGIS para coordenadas GPS
- ✅ Transacciones ACID
- ✅ Excelente rendimiento

---

## 8. Restricciones de Diseño

### 8.1 Arquitectónicas
- Backend: Único proyecto FastAPI modular (no microservicios)
- ETL: Script Docker separado del backend
- Base de datos: PostgreSQL compartida

### 8.2 Tecnológicas
- Python 3.11+, FastAPI
- React 18+, TypeScript, Vite
- PostgreSQL 15+
- Docker y Docker Compose

### 8.3 De Seguridad
- HTTPS obligatorio en producción
- JWT con algoritmo RS256
- Contraseñas con bcrypt (cost factor 12+)
- Cumplimiento OWASP ASVS Nivel 2

### 8.4 Regulatorias
- Ley 1581 de 2012 (Protección de Datos Personales, Colombia)
- WCAG 2.1 Level AA (Accesibilidad)

### 8.5 De Calidad
- Disponibilidad: 99% uptime
- Tiempo de respuesta: <2s (P90)
- Cobertura de tests: >80% backend, >70% frontend

---

## 9. Apéndices

### 9.1 Priorización de Requisitos para MVP

#### Alta Prioridad (Core MVP)
**Sprint 1-2 (Semanas 1-4):**
- RF-001 a RF-005: Autenticación y perfil
- RF-006 a RF-008: Exploración de actividades
- RNF-014, RNF-021: Seguridad básica y Docker

**Sprint 3-4 (Semanas 5-8):**
- RF-009: CRUD actividades (admin)
- RF-011 a RF-013: Favoritos
- RF-014: Recomendaciones básicas
- RNF-004, RNF-005: Optimización de performance

#### Media Prioridad (MVP Extendido)
**Sprint 5-6 (Semanas 9-12):**
- RF-010: Importación manual
- RF-015 a RF-018: Gestión ETL
- RF-021: Dashboard admin
- RNF-019: Tests automatizados

#### Baja Prioridad (Post-MVP)
**Fase 2:**
- RF-019 a RF-020: Dispositivos IoT
- RF-022: Gestión avanzada usuarios
- Recomendaciones avanzadas (filtrado colaborativo)

---

### 9.2 Métricas de Éxito del MVP

| Métrica | Objetivo | Método de Medición |
|---------|----------|-------------------|
| Usuarios registrados | ≥200 | Analytics, BD |
| Actividades en catálogo | ≥150 (70% oferta) | Count en BD |
| CTR recomendaciones | ≥20% | Event tracking |
| NPS | ≥70 | Encuesta post-MVP |
| Tiempo de respuesta API | <2s (P90) | APM, Prometheus |
| Disponibilidad | ≥99% | Uptime monitoring |
| Cobertura de tests | >80% backend | Coverage reports |

---

### 9.3 Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| APIs públicas no disponibles | Media | Alto | Caché de datos, ETL con retry logic |
| Bajo rendimiento con escala | Media | Alto | Índices BD, paginación, caché Redis |
| Vulnerabilidades de seguridad | Media | Crítico | SAST/DAST, auditorías, OWASP ASVS |
| Adopción baja de usuarios | Alta | Alto | UX testing, marketing, onboarding |
| Retraso en desarrollo | Media | Medio | Priorización clara, MVP lean |

---

### 9.4 Glosario

| Término | Definición |
|---------|------------|
| **MVP** | Minimum Viable Product - Producto mínimo viable |
| **SOA** | Service-Oriented Architecture - Arquitectura orientada a servicios |
| **ETL** | Extract, Transform, Load - Proceso de ingesta de datos |
| **JWT** | JSON Web Token - Token de autenticación |
| **CRUD** | Create, Read, Update, Delete - Operaciones básicas |
| **API** | Application Programming Interface |
| **REST** | Representational State Transfer |
| **IoT** | Internet of Things |
| **IDRD** | Instituto Distrital de Recreación y Deporte |
| **WCAG** | Web Content Accessibility Guidelines |
| **OWASP** | Open Web Application Security Project |
| **NPS** | Net Promoter Score |
| **RTO** | Recovery Time Objective |
| **RPO** | Recovery Point Objective |

---

### 9.5 Referencias y Documentos Relacionados

1. **Triqueta_Contexto_Proyecto.md** - Contexto general del proyecto
2. **SRS_Requisitos_Funcionales.md** - Especificación detallada de requisitos funcionales
3. **SRS_Requisitos_No_Funcionales.md** - Especificación detallada de requisitos no funcionales
4. **SRS_Arquitectura_y_Datos.md** - Arquitectura y modelo de datos

**Estándares de referencia:**
- ISO/IEC/IEEE 29148:2018 - Requirements engineering
- ISO/IEC 25010:2023 - Software quality model
- OWASP ASVS v5.0 - Security verification
- WCAG 2.1 Level AA - Accessibility
- RFC 6749 - OAuth 2.0
- RFC 7519 - JWT

---

## 10. Aprobaciones y Control de Cambios

### 10.1 Firmas de Aprobación

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Product Owner | [Nombre] | [Fecha] | _______ |
| Arquitecto de Software | [Nombre] | [Fecha] | _______ |
| Líder de Desarrollo | [Nombre] | [Fecha] | _______ |
| QA Lead | [Nombre] | [Fecha] | _______ |

### 10.2 Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | Oct 2025 | Equipo Diseño Creativo | Versión inicial del SRS |

---

**Fin del documento - Software Requirements Specification (SRS)**

**Proyecto:** Triqueta Digital  
**Versión:** 1.0  
**Fecha:** Octubre 2025  
**Estándar:** ISO/IEC/IEEE 29148:2018

