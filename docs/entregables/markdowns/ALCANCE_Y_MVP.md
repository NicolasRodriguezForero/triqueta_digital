# Alcance del Proyecto y Definición del MVP

**Proyecto:** Triqueta Digital  
**Versión:** 1.0  
**Fecha:** Octubre 2025

---

## 1. Alcance del Proyecto

### 1.1 Alcance Funcional

Triqueta Digital es una plataforma web que conecta actividades culturales, recreativas y deportivas en las localidades de Chapinero, Santa Fe y La Candelaria (Bogotá).

#### Módulos Incluidos:

**1. Autenticación y Gestión de Usuarios**

- Registro con email y contraseña
- Inicio y cierre de sesión
- Recuperación de contraseña
- Renovación automática de tokens (OAuth2 + JWT)
- Gestión de sesiones seguras

**2. Exploración de Actividades**

- Listado público de actividades con paginación
- Búsqueda full-text (título, descripción, etiquetas)
- Filtros múltiples: tipo, localidad, fecha, precio, nivel, etiquetas
- Vista detallada de actividad
- Registro de vistas para popularidad

**3. Sistema de Favoritos**

- Guardar/eliminar actividades favoritas
- Listado de favoritos del usuario
- Sincronización con sistema de recomendaciones

**4. Recomendaciones Personalizadas (IA)**

- Algoritmo híbrido: popularidad + etiquetas + localidad + disponibilidad
- Explicaciones de por qué se recomienda
- Caché en Redis para optimización

**5. Perfil de Usuario**

- Visualización y edición de perfil
- Preferencias: etiquetas de interés, localidad, disponibilidad horaria, nivel de actividad

**6. Panel de Administración**

- CRUD completo de actividades
- Dashboard con métricas clave
- Gestión de usuarios (roles y estados)
- Validación de actividades importadas
- Visualización de logs y reportes

**7. Gestión de Ingesta (ETL)**

- Importación manual: CSV y JSON
- Importación automática desde fuentes públicas (API IDRD, portales distritales)
- Validación y normalización de datos
- Detección de duplicados
- Programación de ejecuciones automáticas
- Logs detallados de procesos

**8. Dispositivos IoT**

- Vinculación de dispositivo cúbico a cuenta de usuario
- API de sincronización para obtener recomendaciones
- Token JWT específico para dispositivos

---

### 1.2 Alcance No Funcional

#### Usabilidad

- Interfaz responsive (mobile-first)
- Accesibilidad WCAG 2.1 Level AA (>95% cumplimiento)
- Diseño moderno con Shadcn UI y TailwindCSS
- Experiencia de usuario fluida y consistente

#### Performance

- Tiempo de respuesta API < 2s en P90 (percentil 90)
- Core Web Vitals: LCP <2.5s, FID <100ms, CLS <0.1
- Disponibilidad del sistema: 99% uptime
- Optimización de queries con índices PostgreSQL
- Caché estratégico con Redis

#### Seguridad

- OAuth2 Password Grant + JWT (RS256)
- Hash de contraseñas con bcrypt
- Rate limiting en endpoints críticos (autenticación, APIs públicas)
- Validación de entrada (Pydantic schemas)
- Protección contra OWASP Top 10
- HTTPS obligatorio en producción
- Cumplimiento Ley 1581/2012 (Protección de Datos Colombia)

#### Compatibilidad

- Navegadores: Chrome, Firefox, Safari, Edge (últimas 2 versiones)
- Dispositivos: Desktop, tablet, móvil
- PWA (Progressive Web App) para instalación en móvil

#### Mantenibilidad

- Código documentado (docstrings en Python, JSDoc en TypeScript)
- Complejidad ciclomática <10 promedio
- Arquitectura SOA modular
- Separación clara de responsabilidades (servicios, controladores, modelos)
- Tests unitarios y de integración

#### Portabilidad

- Containerización completa con Docker
- Docker Compose para desarrollo local
- CI/CD con GitHub Actions
- Deploy automatizado

---

### 1.3 Fuera de Alcance

Las siguientes funcionalidades **NO están incluidas** en el proyecto actual:

**Funcionalidades Excluidas:**

- Sistema de reservas o compra de tickets
- Pasarela de pagos integrada
- Chat en vivo o mensajería entre usuarios
- Sistema de comentarios y calificaciones de actividades
- Red social (seguir usuarios, compartir en redes)
- Notificaciones push móviles nativas
- App móvil nativa (iOS/Android)
- Integración con calendarios externos (Google Calendar, Outlook)
- Gamificación (puntos, badges, rankings)
- Múltiples idiomas (i18n)
- Panel analítico avanzado con BI
- Exportación de reportes en PDF/Excel
- Sistema de roles granular (solo admin/usuario)
- Geolocalización en tiempo real
- Mapa interactivo avanzado con rutas

**Integraciones Excluidas:**

- Redes sociales (login con Google, Facebook, etc.)
- Servicios de terceros (Mailchimp, Analytics avanzados)
- APIs de clima o tráfico

---

### 1.4 Supuestos y Restricciones

#### Supuestos:

- Las fuentes de datos públicas (IDRD, portales distritales) mantienen disponibilidad >90%
- Los usuarios tienen acceso a internet y dispositivos compatibles
- La información de actividades proviene de fuentes confiables
- El equipo tiene acceso a infraestructura cloud o servidores para deployment
- Se dispone de tiempo completo del equipo durante las 9 semanas

#### Restricciones:

- **Tiempo:** 9 semanas (22 sept - 22 nov 2025)
- **Equipo:** 5 personas (2 backend, 2 frontend, 1 DevOps/QA)
- **Presupuesto:** Limitado a herramientas gratuitas/open-source
- **Alcance geográfico:** Solo 3 localidades de Bogotá (Chapinero, Santa Fe, La Candelaria)
- **Stack tecnológico:** Definido (no cambios mayores permitidos)
- **Datos:** Dependencia de fuentes públicas para catálogo inicial

#### Dependencias:

- API IDRD disponible y estable
- Portales distritales con datos actualizados
- Servicios de infraestructura (hosting, base de datos)
- Librerías y frameworks de código abierto

---

### 1.5 Stakeholders y Usuarios

#### Stakeholders:

- **Equipo de desarrollo:** Responsables de implementar la plataforma
- **Universidad/Docentes:** Supervisión académica del proyecto
- **Comunidad local:** Organizadores de actividades culturales/deportivas
- **Alcaldías locales:** Proveedores de información de actividades

#### Usuarios Finales:

- **Ciudadanos de Bogotá:** Personas que buscan actividades en las 3 localidades
- **Administradores de la plataforma:** Gestionan catálogo y usuarios
- **Usuarios del dispositivo IoT:** Personas con el cubo físico vinculado

#### Perfil de Usuario Principal:

- Edad: 18-45 años
- Ubicación: Bogotá (Chapinero, Santa Fe, La Candelaria)
- Intereses: Cultura, deporte, recreación
- Nivel tecnológico: Medio (uso habitual de web/apps)

---

## 2. Definición del MVP (Minimum Viable Product)

**Fecha de Entrega MVP:** 2 de Noviembre de 2025

El MVP incluye las funcionalidades esenciales para que la plataforma sea útil y demostrable.

### 2.1 Módulos Incluidos en MVP

#### Autenticación Completa

**Incluye:**

- Registro de usuarios con validación
- Login con OAuth2 + JWT
- Logout y revocación de tokens
- Renovación automática de sesión

**Excluye del MVP:**

- Recuperación de contraseña (post-MVP)
- Login social (fuera de alcance)

---

#### Exploración de Actividades

**Incluye:**

- Listado público con paginación (20 por página)
- Búsqueda full-text optimizada
- Filtros: tipo, localidad, fecha, precio, nivel, etiquetas
- Vista detallada de actividad
- Registro de vistas para popularidad

**Excluye del MVP:**

- Mapa interactivo (opcional)
- Compartir en redes sociales (fuera de alcance)

---

#### Sistema de Favoritos

**Incluye:**

- Guardar/eliminar favoritos
- Listado de favoritos del usuario
- Botón de favorito integrado en tarjetas
- Actualización de popularidad al guardar

**Excluye del MVP:**

- Colecciones o listas personalizadas (fuera de alcance)
- Compartir favoritos con otros usuarios (fuera de alcance)

---

#### Recomendaciones IA (Básicas)

**Incluye:**

- Algoritmo híbrido simplificado
- Top 10 recomendaciones personalizadas
- Explicaciones de por qué se recomienda
- Caché básico en Redis

**Excluye del MVP:**

- Machine Learning avanzado (post-MVP)
- A/B testing de algoritmos (post-MVP)
- Feedback explícito sobre recomendaciones (post-MVP)

---

#### Perfil de Usuario (Básico)

**Incluye:**

- Visualizar perfil propio
- Editar: nombre, etiquetas de interés, localidad preferida

**Excluye del MVP:**

- Foto de perfil (post-MVP)
- Disponibilidad horaria compleja (post-MVP)
- Privacidad granular (post-MVP)

---

#### Panel de Administración (Core)

**Incluye:**

- CRUD de actividades (crear, editar, eliminar)
- Importación manual CSV/JSON
- Validación de actividades importadas
- Listado de usuarios (solo visualización)

**Excluye del MVP:**

- Dashboard con métricas (post-MVP)
- Gestión avanzada de usuarios (post-MVP)
- Logs detallados de auditoría (post-MVP)

---

### 2.2 Módulos Post-MVP

Los siguientes módulos se implementarán **después del MVP** (3-22 nov):

#### Dashboard de Administración

- Métricas clave: usuarios, actividades, interacción
- Gráficos visuales (torta, barras)
- Top actividades y etiquetas

#### ETL Automatizado

- Script ETL completo en Docker separado
- Extractor API IDRD
- Transformer y Loader
- Programación automática
- Gestión de procesos desde admin

#### Dispositivos IoT

- Vinculación de dispositivo
- API de sincronización
- Token JWT para dispositivos

#### Mejoras de Perfil

- Foto de perfil
- Disponibilidad horaria
- Configuración de privacidad

#### Mejoras de Admin

- Gestión completa de usuarios (cambiar roles, estados)
- Logs de auditoría
- Reportes exportables

---

### 2.3 Criterios de Aceptación del MVP

El MVP se considera **completo y aceptado** si cumple:

**Funcionalidad:**

- Todas las historias de usuario de prioridad ALTA implementadas
- Flujo completo funcional: registro → explorar → favoritos → recomendaciones
- Panel admin permite CRUD de actividades e importación CSV/JSON

**Calidad:**

- Cobertura de tests backend >70%
- Cobertura de tests frontend >60%
- 0 bugs críticos o bloqueantes
- Lighthouse Accessibility >90

**Performance:**

- API P90 <2s en búsquedas
- Página de actividades carga en <3s

**Datos:**

- Base de datos con mínimo 100 actividades
- Al menos 2 fuentes de datos (manual + CSV/JSON importado)

**Deployment:**

- MVP deployado en ambiente de staging
- Accesible vía URL pública
- Docker Compose funcional para desarrollo

---

## 3. Métricas de Éxito

### 3.1 Métricas al Finalizar MVP (2 Nov 2025)

#### Métricas Técnicas

| Métrica                       | Rango Objetivo | Método de Medición          |
| ----------------------------- | -------------- | --------------------------- |
| Tiempo de respuesta API (P90) | 1.5s - 2.5s    | Logs de backend, monitoring |
| Uptime del sistema            | 95% - 99%      | Monitoring de servidor      |
| Cobertura de tests backend    | 70% - 85%      | Coverage report (pytest)    |
| Cobertura de tests frontend   | 60% - 75%      | Coverage report (Vitest)    |
| Bugs críticos                 | 0 - 2          | Issue tracker (GitHub)      |
| Bugs menores                  | 0 - 10         | Issue tracker (GitHub)      |
| Lighthouse Performance        | 75 - 90        | Lighthouse audit            |
| Lighthouse Accessibility      | 90 - 100       | Lighthouse audit            |
| Core Web Vitals (LCP)         | 2.0s - 3.0s    | Lighthouse/Web Vitals       |

#### Métricas de Negocio

| Métrica                     | Rango Objetivo | Método de Medición                             |
| --------------------------- | -------------- | ---------------------------------------------- |
| Actividades en catálogo     | 100 - 200      | Query a base de datos                          |
| Fuentes de datos integradas | 2 - 3          | Configuración ETL                              |
| Localidades cubiertas       | 3              | Dato fijo (Chapinero, Santa Fe, La Candelaria) |
| Tipos de actividades        | 3              | Dato fijo (Cultura, Deporte, Recreación)       |
| Etiquetas únicas            | 20 - 40        | Query a base de datos                          |

#### Métricas de Usuario (Testing Interno)

| Métrica                             | Rango Objetivo | Método de Medición    |
| ----------------------------------- | -------------- | --------------------- |
| Usuarios de prueba registrados      | 10 - 25        | Query a base de datos |
| Actividades marcadas como favoritas | 20 - 60        | Query a base de datos |
| Búsquedas realizadas                | 30 - 100       | Logs de backend       |
| Tiempo promedio en plataforma       | 3min - 8min    | Analytics básico      |
| Tasa de éxito en registro           | 85% - 100%     | Logs + encuesta       |

#### Métricas de Proyecto

| Métrica                                 | Rango Objetivo | Método de Medición       |
| --------------------------------------- | -------------- | ------------------------ |
| Cumplimiento de cronograma MVP          | 90% - 100%     | Comparación plan vs real |
| Historias de usuario completadas (Alta) | 14 - 16        | Seguimiento de tareas    |
| Commits en repositorio                  | 200 - 400      | GitHub stats             |
| Pull requests mergeados                 | 40 - 80        | GitHub stats             |
| Code reviews realizados                 | 100% PRs       | GitHub stats             |

---

### 3.2 Métricas al Finalizar Proyecto Completo (22 Nov 2025)

#### Métricas Técnicas

| Métrica                          | Rango Objetivo | Método de Medición   |
| -------------------------------- | -------------- | -------------------- |
| Tiempo de respuesta API (P90)    | <2s            | Logs de backend, APM |
| Uptime del sistema               | 99% - 99.9%    | Monitoring 24/7      |
| Cobertura de tests backend       | 80% - 90%      | Coverage report      |
| Cobertura de tests frontend      | 70% - 85%      | Coverage report      |
| Bugs críticos en producción      | 0              | Issue tracker        |
| Bugs menores                     | 0 - 5          | Issue tracker        |
| Lighthouse Performance (desktop) | 90 - 100       | Lighthouse audit     |
| Lighthouse Performance (mobile)  | 80 - 95        | Lighthouse audit     |
| Lighthouse Accessibility         | 95 - 100       | Lighthouse audit     |
| Core Web Vitals (LCP)            | <2.5s          | Real user monitoring |
| Core Web Vitals (FID)            | <100ms         | Real user monitoring |
| Core Web Vitals (CLS)            | <0.1           | Real user monitoring |
| Vulnerabilidades críticas (SAST) | 0              | Security scan        |
| Deuda técnica                    | Baja - Media   | SonarQube o similar  |

#### Métricas de Negocio

| Métrica                                | Rango Objetivo | Método de Medición        |
| -------------------------------------- | -------------- | ------------------------- |
| Actividades en catálogo                | 150 - 300      | Query a base de datos     |
| Actividades activas (vigentes)         | 80 - 200       | Query con filtro de fecha |
| Fuentes de datos integradas            | 3 - 5          | Configuración ETL         |
| Ejecuciones ETL exitosas               | >90%           | Logs ETL                  |
| Tasa de detección de duplicados        | >85%           | Reporte ETL               |
| Actividades importadas automáticamente | 50 - 150       | Logs ETL                  |

#### Métricas de Usuario (Lanzamiento Limitado)

| Métrica                                | Rango Objetivo | Método de Medición        |
| -------------------------------------- | -------------- | ------------------------- |
| Usuarios registrados totales           | 50 - 150       | Query a base de datos     |
| Usuarios activos (últimos 7 días)      | 30 - 100       | Query con filtro de fecha |
| Actividades favoritas totales          | 100 - 400      | Query a base de datos     |
| Búsquedas realizadas                   | 200 - 800      | Analytics backend         |
| Recomendaciones generadas              | 300 - 1000     | Logs de sistema           |
| Tasa de conversión (visita → favorito) | 5% - 15%       | Cálculo: favoritos/vistas |
| Tiempo promedio en plataforma          | 5min - 12min   | Analytics                 |
| Tasa de rebote                         | 30% - 60%      | Analytics                 |
| Dispositivos IoT vinculados            | 5 - 20         | Query a base de datos     |
| Satisfacción de usuario (encuesta)     | 7/10 - 9/10    | Encuesta post-uso         |

#### Métricas de Proyecto

| Métrica                                | Rango Objetivo  | Método de Medición       |
| -------------------------------------- | --------------- | ------------------------ |
| Cumplimiento de cronograma total       | 95% - 100%      | Comparación plan vs real |
| Historias de usuario completadas       | 30 - 35 (de 35) | Seguimiento de tareas    |
| Funcionalidades del alcance entregadas | 95% - 100%      | Checklist de alcance     |
| Commits totales                        | 500 - 900       | GitHub stats             |
| Pull requests mergeados                | 100 - 150       | GitHub stats             |
| Líneas de código backend               | 8,000 - 15,000  | Cloc o similar           |
| Líneas de código frontend              | 6,000 - 12,000  | Cloc o similar           |
| Tests unitarios totales                | 80 - 120        | Test runner              |
| Tests E2E                              | 15 - 30         | Playwright               |
| Documentación completa                 | 100%            | Checklist manual         |
| Video demo entregado                   | Sí              | Entregable físico        |

---

### 3.3 Métricas Post-Lanzamiento (Opcional - Futuro)

Estas métricas se medirían **después del proyecto académico**, en caso de lanzamiento público:

#### 1 Mes Post-Lanzamiento:

- Usuarios activos mensuales (MAU): 150 - 300
- Retención de usuarios (día 30): 30% - 50%
- NPS (Net Promoter Score): 60 - 80
- Actividades vistas por usuario: 8 - 15

#### 3 Meses Post-Lanzamiento:

- Usuarios activos mensuales (MAU): 200+ (objetivo inicial del proyecto)
- Crecimiento mensual de usuarios: 10% - 25%
- Actividades en catálogo: 300 - 500
- Cobertura de oferta cultural/deportiva: 50% - 70%
- Engagement (sesiones/usuario/mes): 3 - 6

---

## 4. Estrategia de Validación de Métricas

### 4.1 Herramientas de Medición

**Performance:**

- Lighthouse CI integrado en GitHub Actions
- Logs de backend con timestamps
- PostgreSQL slow query log

**Testing:**

- Pytest con coverage plugin (backend)
- Vitest con coverage (frontend)
- Playwright para E2E

**Monitoreo:**

- Docker logs para uptime
- Prometheus + Grafana (opcional)
- Monitoring manual durante MVP

**Analytics:**

- Logs personalizados en backend
- Query directo a base de datos
- Google Analytics (opcional post-MVP)

**Seguridad:**

- Bandit (SAST para Python)
- Semgrep (SAST general)
- Dependency check (npm audit, safety)

### 4.2 Frecuencia de Medición

**Durante Desarrollo (MVP):**

- Tests: En cada commit (CI)
- Performance: Semanal (manual)
- Bugs: Diario (issue tracking)
- Progreso: Diario (standup)

**Pre-Lanzamiento (Proyecto Completo):**

- Tests: En cada commit (CI)
- Performance: Antes de cada deploy
- Security scan: Semanal
- User testing: 2-3 sesiones antes de entrega

**Post-Lanzamiento:**

- Usuarios/actividad: Diario
- Performance: Semanal
- Satisfacción: Mensual (encuesta)

---

## 5. Criterios de Éxito del Proyecto

El proyecto se considera **exitoso** si cumple:

### Criterios Obligatorios:

1. **Funcionalidad:**

   - MVP completo y funcional al 2 de noviembre
   - 95%+ del alcance definido implementado al 22 de noviembre

2. **Calidad:**

   - 0 bugs críticos en producción
   - Cobertura de tests >80% backend, >70% frontend
   - Lighthouse Accessibility >95

3. **Performance:**

   - API P90 <2s
   - Uptime >99% durante período de evaluación

4. **Datos:**

   - Catálogo con 150-300 actividades reales
   - Al menos 3 fuentes de datos integradas

5. **Entregables:**
   - Código fuente completo en GitHub
   - Aplicación deployada y accesible
   - Documentación técnica completa
   - Video demo del proyecto

### Criterios Deseables:

- Usuarios de prueba >50 registrados
- NPS >70 en encuesta de satisfacción
- Dispositivo IoT funcional y demostrable
- Performance Lighthouse >90 en desktop
