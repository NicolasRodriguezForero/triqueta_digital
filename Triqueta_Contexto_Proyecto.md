# Proyecto: Triqueta Digital

## 1. Visión General

**Triqueta Digital** es una plataforma digital que conecta actividades culturales, recreativas y deportivas en las localidades **Chapinero, Santa Fe y La Candelaria (Bogotá)**.  
El objetivo es **integrar al menos el 70% de la oferta** disponible mediante fuentes públicas y privadas, y **recomendar actividades personalizadas** usando inteligencia artificial.  
El proyecto incluye una **plataforma web/móvil** y un **dispositivo cúbico físico** vinculado a la cuenta del usuario que muestra planes recomendados.

---

## 2. Objetivos del Proyecto

- Centralizar la información dispersa de la oferta cultural y deportiva local.
- Facilitar a los ciudadanos el **descubrimiento y participación** en actividades.
- Generar **recomendaciones personalizadas** basadas en preferencias, ubicación y contexto.
- Fortalecer el vínculo comunitario y la apropiación del territorio.
- Desarrollar un **dispositivo físico (cubo)** que extienda la experiencia digital.

---

## 3. Alcance Funcional (MVP)

### 3.1 Funcionalidades del Usuario

- **Registro/Login**: email y contraseña.
- **Gestión de perfil**: intereses, disponibilidad.
- **Exploración de actividades**:
  - Filtros: tipo, fecha, localidad, precio, nivel de actividad, etc.
  - Búsqueda libre con palabras clave.
- **Recomendaciones personalizadas**:
  - Motor híbrido (contenido + popularidad).
  - Explicaciones simples (“recomendado porque te gustan actividades culturales”).
- **Detalle de actividad**: descripción, horario, ubicación, contacto, mapa.
- **Guardar o marcar favoritos.**

### 3.2 Funcionalidades del Administrador

- **Gestión de catálogo**:
  - CRUD de actividades.
  - Importación desde fuentes públicas (IDRD, portales distritales).
- **Curaduría y validación de datos.**
- **Dashboard** de estadísticas básicas (actividades cargadas, usuarios activos, engagement).

### 3.3 Integración del Dispositivo Cúbico

- Sincronización con la cuenta del usuario.
- Muestra rotativamente 3–5 actividades recomendadas.
- Actualización automática (via API).
- Control táctil o por gesto (según diseño).

---

## 4. Componentes Principales

| Módulo                          | Descripción                                                                       | Dependencias                    |
| ------------------------------- | --------------------------------------------------------------------------------- | ------------------------------- |
| **Frontend Web/Móvil**          | SPA/Progressive Web App para usuarios y administradores.                          | React/Next.js o Flutter         |
| **Backend API**                 | Microservicio REST/GraphQL que centraliza datos, autenticación y recomendaciones. | Node.js (NestJS o Express)      |
| **Base de Datos**               | Almacena usuarios, actividades y registros de interacción.                        | PostgreSQL o MongoDB            |
| **Módulo de Integración (ETL)** | Importa y normaliza datos desde fuentes públicas (CSV, JSON, APIs).               | Python (Pandas, FastAPI)        |
| **Módulo de IA/Recomendación**  | Motor híbrido de recomendación.                                                   | Python (scikit-learn, FastAPI)  |
| **Cubo IoT**                    | Dispositivo conectado vía Wi-Fi o BLE.                                            | ESP32 / Raspberry Pi Pico W     |
| **Panel Administrativo**        | Gestión de contenido, curaduría y métricas.                                       | Integrado en el Frontend        |
| **Infraestructura y DevOps**    | CI/CD, contenedores, monitoreo, seguridad.                                        | Docker, GitHub Actions, AWS/GCP |

---

## 5. Arquitectura Técnica (High Level)

[Usuario Web/Móvil]
↓
[Frontend SPA/PWA]
↓ REST/GraphQL
[Backend API Gateway]
↓
├── [Microservicio: Actividades]
├── [Microservicio: Usuarios]
├── [Microservicio: Recomendador (IA)]
├── [Microservicio: Ingesta/ETL]
└── [Microservicio: Cubo IoT Handler]
↓
[DB Principal (PostgreSQL/Mongo)]
↓
[Analítica y Observabilidad]

- **Autenticación:** JWT + OAuth2.
- **Seguridad:** OWASP ASVS v5.0 nivel 2 + ISO/IEC 27001 (controles de autenticación, sesiones, cifrado, logging).
- **Infraestructura recomendada:** Contenedores Docker, CI/CD automatizado, monitoreo Prometheus/Grafana.

---

## 6. Requisitos No Funcionales (ISO/IEC 25010:2023)

| Categoría                    | Subcaracterística           | Métrica / Criterio       |
| ---------------------------- | --------------------------- | ------------------------ |
| **Usabilidad**               | Accesibilidad AA (WCAG 2.1) | Cumplimiento >95%        |
| **Eficiencia**               | Tiempo de respuesta         | < 2s en 90% de requests  |
| **Fiabilidad**               | Disponibilidad              | 99% uptime               |
| **Mantenibilidad**           | Complejidad por módulo      | <10 CC promedio          |
| **Seguridad**                | Cumplimiento ASVS nivel 2   | Verificado por checklist |
| **Compatibilidad**           | Multiplataforma             | Web + móvil PWA          |
| **Portabilidad**             | Contenedores Docker         | CI/CD verificado         |
| **Satisfacción del usuario** | NPS                         | >70                      |

---

## 7. IA: Módulo de Recomendación

### 7.1 Objetivo

Recomendar actividades basadas en:

- Preferencias declaradas (intereses, horario, localidad).
- Popularidad general.
- Histórico de interacciones (guardados, asistencias).

### 7.2 Enfoque

- **Fase 1 (MVP):** Recomendador híbrido (content-based + popularidad).
- **Fase 2:** Incorporar filtrado colaborativo y embeddings semánticos.
- **Métricas:** Precision@k, diversidad, tasa de conversión.
- **Explicabilidad:** Etiquetas simples visibles (“por tus intereses en arte y cultura”).

---

## 8. Pipeline de Datos (ETL)

1. **Extracción**
   - APIs públicas: IDRD, Portales Distritales, fuentes CSV/JSON.
2. **Transformación**
   - Limpieza, deduplicación, normalización de campos.
   - Categorización estándar (cultura, deporte, recreación, etc.).
3. **Carga**
   - Inserción en base unificada de actividades.
   - Registro de fuente y confiabilidad.
4. **Actualización Automática**
   - Cron jobs diarios/semanales.

---

## 9. Seguridad y Cumplimiento

- **ISO/IEC 27001:2022** — Gestión de seguridad de la información.
- **OWASP ASVS v5.0** — Requisitos técnicos de seguridad en autenticación, control de acceso y cifrado.
- **Política de Datos Personales** — Cumplimiento con la Ley 1581 de 2012 (Colombia).
- **Modelo de amenazas STRIDE.**
- **Pruebas SAST y DAST** integradas en CI/CD.

---

## 10. Plan de Iteración 1 (MVP Técnico)

**Duración estimada:** 6–8 semanas.  
**Objetivo:** Validar hipótesis de uso y atractivo del sistema.

### Alcance Iteración 1:

1. Módulo de autenticación (registro, login, perfil básico).
2. Explorador de actividades (listado, detalle, filtros).
3. Módulo de administración (carga manual + importación básica).
4. Módulo de recomendaciones (versión inicial).
5. API pública (REST/GraphQL).
6. Prototipo del dispositivo cúbico (interfaz básica + sincronización).

**Entregables clave:**

- Sistema desplegado (entorno staging).
- 50–100 actividades de prueba cargadas.
- 20 usuarios de prueba.
- Métricas básicas de uso (CTR, búsquedas, guardados).

---

## 11. Stack Tecnológico Propuesto

| Capa            | Tecnología                           | Alternativas        |
| --------------- | ------------------------------------ | ------------------- |
| Frontend        | React + Next.js / Tailwind           | Flutter Web         |
| Backend         | Node.js (NestJS) / FastAPI (Python)  | Django REST         |
| BD              | PostgreSQL                           | MongoDB             |
| Infraestructura | Docker + GitHub Actions + AWS/GCP    | Render/Fly.io       |
| IA              | Python (scikit-learn, pandas, numpy) | TensorFlow Lite     |
| IoT             | ESP32 / Raspberry Pi Pico W          | Arduino Nano 33 IoT |
| Analytics       | Plausible / Mixpanel / Grafana       | Google Analytics 4  |

---

## 12. Referencias Normativas y de Buenas Prácticas

| Estándar / Marco            | Uso en el Proyecto                     |
| --------------------------- | -------------------------------------- |
| **ISO/IEC/IEEE 29148:2018** | Requisitos y trazabilidad              |
| **ISO/IEC 25010:2023**      | Calidad del producto software          |
| **OWASP ASVS v5.0**         | Requisitos de seguridad                |
| **ISO/IEC 27001:2022**      | Gestión de seguridad de la información |
| **Scrum Guide 2020**        | Metodología ágil                       |
| **WCAG 2.1 AA**             | Accesibilidad                          |
| **IEEE 830-1998**           | Estructura del SRS base                |

---

## 13. Métricas de Éxito (MVP)

| Métrica                    | Descripción               | Umbral de éxito            |
| -------------------------- | ------------------------- | -------------------------- |
| Usuarios activos           | Usuarios únicos mensuales | ≥ 200                      |
| Actividades registradas    | Fuente IDRD + manual      | ≥ 70% de oferta disponible |
| CTR de recomendaciones     | % de clics en sugerencias | ≥ 20%                      |
| Tiempo de respuesta        | Promedio API < 2s         | ✅                         |
| Satisfacción usuario (NPS) | Encuesta piloto           | ≥ 70                       |

---

## 14. Roadmap de Fases Posteriores (visión)

| Fase   | Enfoque                                        | Duración estimada |
| ------ | ---------------------------------------------- | ----------------- |
| Fase 2 | Recomendador avanzado + reputación comunitaria | 8–10 semanas      |
| Fase 3 | Integración completa con fuentes distritales   | 6–8 semanas       |
| Fase 4 | Gamificación y logros                          | 6 semanas         |
| Fase 5 | Despliegue ampliado a otras localidades        | 8–12 semanas      |

---

## 15. Archivos y Artefactos Esperados

- `/docs/SRS.md` — Especificación de Requisitos (ISO/IEC/IEEE 29148).
- `/docs/NFR_Matrix.md` — Mapeo ISO/IEC 25010.
- `/src/api/` — Backend modular (Node/FastAPI).
- `/src/frontend/` — WebApp React/Next.js.
- `/src/recommender/` — Motor IA inicial.
- `/src/device/` — Firmware del cubo IoT.
- `/infra/` — Dockerfiles, CI/CD, IaC scripts.
- `/tests/` — Unit, e2e, security tests.
- `/README.md` — Guía de despliegue y entorno.

---

## 16. Licencia y Propiedad Intelectual

- Propiedad del proyecto: **Diseño Creativo / Entidad académica responsable.**
- Uso de código abierto recomendado bajo licencia **MIT o Apache 2.0** (según dependencias).
- Datos públicos respetan licencias de origen (IDRD, bogota.gov.co).

---

## 17. Autor y Contexto

- **Proyecto académico aplicado** dentro del marco de Diseño Creativo.
- Supervisión técnica: especialista en diseño y desarrollo de software.
- Referencia documental: _Planteamiento del Proyecto.pdf_.
- Fecha base: Octubre 2025.

---

## 18. Resumen para agentes automáticos

**Entrada esperada:**

- Archivos de requisitos (SRS, NFR, backlog).
- Fuentes de datos (CSV, API).

**Salida esperada:**

- Código funcional MVP.
- Infraestructura dockerizada.
- Logs y métricas operativas.
- Documentación técnica actualizada.

---

> **Nota:** Este documento sirve como _context file_ para asistentes de desarrollo o coding agents.  
> Está optimizado para comprender alcance, objetivos, arquitectura, componentes y entregables de la **primera iteración** del proyecto Triqueta Digital.
