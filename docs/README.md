# Documentación Técnica - Triqueta Digital

## Descripción General

Documentación completa del proyecto Triqueta Digital, plataforma digital que conecta actividades culturales, recreativas y deportivas en las localidades de Chapinero, Santa Fe y La Candelaria (Bogotá, Colombia).

---

## Estructura de Carpetas

```
docs/
├── entregables/              # Documentos finales del proyecto
│   ├── markdowns/           # Versiones editables en Markdown
│   └── pdfs/                # Versiones finales en PDF
├── varios/                  # Documentos de trabajo y borradores
└── README.md               # Este archivo
```

---

## Documentos Entregables

### Formato Markdown

Ubicación: `docs/entregables/markdowns/`

#### 1. Especificaciones Técnicas

**Archivo:** [Especificaciones_Tecnicas.md](./entregables/markdowns/Especificaciones_Tecnicas.md)

Documento unificado que contiene:

- **Diagrama de Casos de Uso:** Representación visual de interacciones del sistema
- **Historias de Usuario (35):** Casos de uso detallados organizados por módulos
  - Autenticación y Gestión de Usuarios (5)
  - Actividades (8)
  - Favoritos (3)
  - Recomendaciones - IA (2)
  - Perfil de Usuario (2)
  - Administración (9)
  - Gestión de Ingesta - ETL (4)
  - Dispositivos IoT (2)
- **Requisitos Funcionales (RF-001 a RF-022):** Especificaciones técnicas detalladas
- **Requisitos No Funcionales (RNF-001 a RNF-024):** Basados en ISO/IEC 25010:2023
  - Usabilidad
  - Eficiencia de Desempeño
  - Compatibilidad
  - Fiabilidad
  - Seguridad
  - Mantenibilidad
  - Portabilidad
  - Satisfacción del Usuario

#### 2. Arquitectura de Software

**Archivo:** [ARQUITECTURA.md](./entregables/markdowns/ARQUITECTURA.md)

Contiene:

- Estilo arquitectónico (SOA Modular)
- Stack tecnológico completo
- Estructura de directorios del proyecto
- Decisiones arquitectónicas clave
- Diagramas de componentes

#### 3. Alcance y MVP

**Archivo:** [ALCANCE_Y_MVP.md](./entregables/markdowns/ALCANCE_Y_MVP.md)

Contiene:

- Definición del alcance del proyecto
- Características del MVP (Producto Mínimo Viable)
- Funcionalidades incluidas y excluidas
- Criterios de éxito

#### 4. Cronograma Simplificado

**Archivo:** [CRONOGRAMA_SIMPLIFICADO.md](./entregables/markdowns/CRONOGRAMA_SIMPLIFICADO.md)

Contiene:

- Fases de desarrollo
- Timeline del proyecto
- Hitos principales
- Entregables por fase

---

### Formato PDF

Ubicación: `docs/entregables/pdfs/`

Versiones finales en formato PDF para presentación:

| Documento                                  | Descripción                           |
| ------------------------------------------ | ------------------------------------- |
| **Especificaciones_Tecnicas.pdf**          | Especificaciones técnicas completas   |
| **ARQUITECTURA DE SOFTWARE.pdf**           | Arquitectura y diseño del sistema     |
| **CRONOGRAMA_DE_DESARROLLO.pdf**           | Planificación temporal del proyecto   |
| **MODELO RELACIONAL DE BASE DE DATOS.pdf** | Diseño de la base de datos PostgreSQL |
| **PLANIFICACION_DEL_PROYECTO.pdf**         | Planificación general del proyecto    |

---

## Documentos de Trabajo

Ubicación: `docs/varios/`

Esta carpeta contiene documentos de trabajo, borradores y recursos adicionales:

- **casos_de_uso.png:** Diagrama de casos de uso
- **CRONOGRAMA.md:** Cronograma detallado
- **HISTORIAS_USUARIO.md:** Historias de usuario (versión borrador)
- **SRS.md:** Software Requirements Specification (versión borrador)
- **SRS_Requisitos_Funcionales.md:** Requisitos funcionales (versión borrador)
- **SRS_Requisitos_No_Funcionales.md:** Requisitos no funcionales (versión borrador)
- **SRS_Arquitectura_y_Datos.md:** Arquitectura y modelo de datos (versión borrador)

> **Nota:** Para consultar la documentación oficial, utilizar los archivos de la carpeta `entregables/`.

---

## Resumen Ejecutivo del Proyecto

### Objetivos Principales

- Integrar al menos 70% de la oferta cultural y deportiva disponible
- Proveer recomendaciones personalizadas mediante IA
- Facilitar participación ciudadana en actividades locales
- MVP con 200+ usuarios activos mensuales

### Stack Tecnológico

**Frontend:**

```
React 18+ + Vite + TypeScript
TailwindCSS + Shadcn UI
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

- Servicio de Autenticación
- Servicio de Usuarios
- Servicio de Actividades
- Servicio de Recomendaciones (IA)
- Servicio de Favoritos
- Servicio de Gestión de Ingesta (ETL)
- Servicio de Dispositivos IoT
- Servicio de Administración

---

## Métricas de Éxito

| Métrica                     | Objetivo          | Método         |
| --------------------------- | ----------------- | -------------- |
| **Usuarios registrados**    | ≥200              | Analytics, BD  |
| **Actividades en catálogo** | ≥150 (70% oferta) | Count BD       |
| **CTR recomendaciones**     | ≥20%              | Event tracking |
| **NPS**                     | ≥70               | Encuesta       |
| **Tiempo respuesta API**    | <2s (P90)         | APM            |
| **Disponibilidad**          | ≥99%              | Monitoring     |
| **Cobertura tests**         | >80% backend      | Coverage       |

---

## Cumplimiento Normativo

- **ISO/IEC/IEEE 29148:2018** - Requirements engineering
- **ISO/IEC 25010:2023** - Software quality model
- **OWASP ASVS v5.0 Nivel 2** - Security verification
- **WCAG 2.1 Level AA** - Accessibility
- **Ley 1581 de 2012** - Protección de Datos Personales (Colombia)
- **RFC 6749** - OAuth 2.0
- **RFC 7519** - JWT

---

## Roadmap de Desarrollo

### Fase 1: MVP Core (Semanas 1-4)

- Autenticación y perfil de usuario
- Exploración de actividades con filtros
- Búsqueda full-text
- Docker Compose setup

### Fase 2: MVP Funcional (Semanas 5-8)

- CRUD de actividades (admin)
- Sistema de favoritos
- Recomendaciones básicas (IA)
- Optimización de performance

### Fase 3: MVP Completo (Semanas 9-12)

- Importación manual de actividades
- Gestión ETL
- Dashboard administrativo
- Tests automatizados

### Fase 4: Post-MVP (Futuro)

- Integración con dispositivo IoT
- Recomendaciones avanzadas (filtrado colaborativo)
- Gamificación
- Expansión a otras localidades

---

## Características Principales

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

## Decisiones Arquitectónicas Clave

| Decisión                            | Justificación                                     |
| ----------------------------------- | ------------------------------------------------- |
| **SOA Modular (no microservicios)** | Simplicidad operacional, desarrollo rápido en MVP |
| **PostgreSQL**                      | Relacional + flexible (JSONB, arrays, PostGIS)    |
| **FastAPI**                         | Alto rendimiento, async, type-safe, OpenAPI auto  |
| **React + Vite**                    | Ecosistema maduro, DX excelente, build rápido     |
| **Docker Compose**                  | Portabilidad, consistencia dev-prod               |
| **ETL Separado**                    | Desacoplamiento, ejecuciones independientes       |
| **JWT con RS256**                   | Stateless, escalable, asimétrico seguro           |
| **OAuth2 Password Grant**           | Estándar, extensible a Social Auth futuro         |

---

## Enlaces Útiles

- [Contexto del Proyecto](../Triqueta_Contexto_Proyecto.md)
- [Plan de Implementación](../PLAN_IMPLEMENTACION.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Equipo y Contacto

**Proyecto:** Diseño Creativo - 8vo Semestre  
**Universidad:** Universidad Sergio Arboleda  
**Fecha:** Octubre 2025

---

## Licencia

Este proyecto es de carácter académico. Consultar con la entidad académica responsable para uso y distribución.

---

## Versión del Documento

**Versión:** 1.0  
**Última actualización:** 22 de Octubre de 2025  
**Estado:** Aprobado para desarrollo

---

## Cómo Usar Esta Documentación

### Para Desarrolladores

1. Comenzar con **Especificaciones_Tecnicas.md** para entender requisitos
2. Revisar **ARQUITECTURA.md** para comprender diseño del sistema
3. Consultar **ALCANCE_Y_MVP.md** para priorizar funcionalidades
4. Seguir **CRONOGRAMA_SIMPLIFICADO.md** para planificación

### Para Stakeholders

- Los documentos PDF en `entregables/pdfs/` están listos para presentación
- Cada PDF corresponde a un aspecto específico del proyecto
- Comenzar con **PLANIFICACION_DEL_PROYECTO.pdf** para visión general

### Para Evaluación Académica

- Todos los entregables están en `entregables/`
- Formatos disponibles: Markdown (editable) y PDF (presentación)
- Cumple con estándares ISO/IEC requeridos
- Incluye diagramas, especificaciones técnicas y planificación completa

---

**¿Preguntas sobre la documentación?**  
Revisa primero los documentos detallados en la carpeta `entregables/`. Si persisten dudas, consulta con el equipo técnico.
