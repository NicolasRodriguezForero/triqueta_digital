# Arquitectura del Sistema - Triqueta Digital

**Proyecto:** Triqueta Digital  
**Versión:** 1.0  
**Fecha:** Octubre 2025  
**Tipo de Arquitectura:** SOA Modular (Monolito Modular con Servicios Internos)

---

## 1. Visión General de la Arquitectura

### 1.1 Patrón Arquitectónico

**Service-Oriented Architecture (SOA) Modular**

La aplicación utiliza una arquitectura de servicios orientada modularmente, donde el backend actúa como un monolito modular con servicios internos bien definidos y separados por responsabilidades.

### 1.2 Principios de Diseño

- **Separación de responsabilidades:** Cada módulo tiene una función específica
- **Independencia de capas:** Frontend y backend completamente desacoplados
- **API First:** Toda comunicación a través de API REST
- **Stateless:** El backend no mantiene estado de sesión (JWT)
- **Cacheable:** Uso estratégico de Redis para optimización
- **Containerización:** Todos los servicios en contenedores Docker

---

## 2. Diagrama de Componentes Principales

### 2.1 Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Usuario)                         │
│                   Navegador Web / Dispositivo IoT                │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         NGINX (Reverse Proxy)                    │
│                 - Routing                                        │
│                 - SSL/TLS                                        │
│                 - Load Balancing (futuro)                        │
└─────────────────────────────────────────────────────────────────┘
           │                                │
           │ (Static)                       │ (API)
           ▼                                ▼
┌──────────────────────┐         ┌──────────────────────────┐
│   FRONTEND (React)   │         │   BACKEND (FastAPI)      │
│                      │◄────────┤                          │
│  - React 18 + Vite   │  JSON   │  - Python 3.11+          │
│  - TypeScript        │  REST   │  - FastAPI               │
│  - TailwindCSS       │         │  - SQLAlchemy (async)    │
│  - Tanstack Router   │         │  - Pydantic              │
│  - React Query       │         │  - OAuth2 + JWT          │
│  - Shadcn UI         │         │                          │
└──────────────────────┘         └──────────────────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
         ┌─────────────────┐   ┌─────────────────┐   ┌────────────────┐
         │  PostgreSQL 15+ │   │   Redis Cache   │   │  ETL Service   │
         │                 │   │                 │   │                │
         │  - Base de datos│   │  - Sesiones     │   │  - Python      │
         │  - PostGIS      │   │  - Caché API    │   │  - Extractors  │
         │  - Full-text    │   │  - Rate limit   │   │  - Transform   │
         │    search       │   │  - Recomendac.  │   │  - Loaders     │
         └─────────────────┘   └─────────────────┘   └────────────────┘
                                                                │
                                                                │
                                                      ┌─────────▼──────────┐
                                                      │  Fuentes Externas  │
                                                      │                    │
                                                      │  - API IDRD        │
                                                      │  - Portales Dist.  │
                                                      │  - CSV/JSON        │
                                                      └────────────────────┘
```

---

## 3. Arquitectura por Capas

### 3.1 Capa de Presentación (Frontend)

**Responsabilidad:** Interfaz de usuario y experiencia

**Tecnologías:**
- React 18+ con Vite (build tool)
- TypeScript (tipado estático)
- TailwindCSS (estilos)
- Shadcn UI (componentes)
- Tanstack Router (routing)
- React Query (estado del servidor)
- Axios (cliente HTTP)

**Estructura de Componentes:**
```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── ui/              # Shadcn UI components
│   │   ├── ActivityCard.tsx
│   │   ├── ActivityFilters.tsx
│   │   ├── SearchBar.tsx
│   │   └── ...
│   ├── routes/              # Páginas (file-based routing)
│   │   ├── index.tsx        # Home
│   │   ├── actividades.tsx  # Listado
│   │   ├── favoritos.tsx
│   │   ├── admin/
│   │   └── ...
│   ├── services/            # API clients
│   │   ├── api.ts           # Axios config
│   │   ├── activities.ts
│   │   ├── auth.ts
│   │   └── ...
│   ├── hooks/               # Custom hooks
│   │   ├── useActivities.ts
│   │   ├── useAuth.ts
│   │   └── ...
│   ├── contexts/            # React contexts
│   │   └── AuthContext.tsx
│   └── types/               # TypeScript types
```

**Características:**
- SPA (Single Page Application)
- Client-side routing
- State management con React Query
- Responsive design (mobile-first)
- PWA ready

---

### 3.2 Capa de Aplicación (Backend API)

**Responsabilidad:** Lógica de negocio, autenticación, autorización

**Tecnologías:**
- Python 3.11+
- FastAPI (framework web)
- SQLAlchemy 2.0 (ORM async)
- Pydantic (validación)
- Alembic (migraciones)
- Python-jose (JWT)
- Passlib + Bcrypt (hashing)

**Estructura Modular:**
```
backend/
├── app/
│   ├── api/                 # Endpoints REST
│   │   └── v1/
│   │       ├── auth.py      # Autenticación
│   │       ├── users.py     # Usuarios
│   │       ├── activities.py # Actividades
│   │       ├── favorites.py
│   │       ├── recommendations.py
│   │       ├── admin.py
│   │       └── iot.py
│   ├── core/                # Configuración
│   │   ├── config.py        # Settings
│   │   ├── security.py      # JWT, hash
│   │   └── deps.py          # Dependencies
│   ├── db/                  # Base de datos
│   │   ├── base.py          # Base SQLAlchemy
│   │   └── session.py       # Sessions
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── activity.py
│   │   ├── favorite.py
│   │   └── ...
│   ├── schemas/             # Schemas Pydantic
│   │   ├── user.py
│   │   ├── activity.py
│   │   └── ...
│   ├── services/            # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── activity_service.py
│   │   ├── favorite_service.py
│   │   ├── recommendation_service.py
│   │   ├── activity_import_service.py
│   │   └── ...
│   └── main.py              # Aplicación FastAPI
├── alembic/                 # Migraciones
└── tests/                   # Tests unitarios
```

**Módulos de Servicio:**

1. **Auth Service**
   - Registro de usuarios
   - Login (OAuth2 Password Grant)
   - Generación y validación de JWT
   - Refresh tokens
   - Password reset

2. **Activity Service**
   - CRUD de actividades
   - Búsqueda full-text
   - Filtrado multi-criterio
   - Paginación
   - Registro de vistas

3. **Favorite Service**
   - Guardar/eliminar favoritos
   - Listado de favoritos
   - Actualización de popularidad

4. **Recommendation Service**
   - Algoritmo híbrido
   - Cálculo de scores
   - Generación de explicaciones
   - Cache en Redis

5. **Activity Import Service**
   - Parser CSV/JSON
   - Validación de datos
   - Detección de duplicados
   - Inserción en BD

6. **Admin Service**
   - Gestión de usuarios
   - Dashboard con métricas
   - Validación de actividades

7. **ETL Service** (separado)
   - Extracción de fuentes externas
   - Transformación y normalización
   - Carga en base de datos

---

### 3.3 Capa de Datos (Persistencia)

**Responsabilidad:** Almacenamiento persistente de datos

#### PostgreSQL 15+

**Base de datos relacional principal**

**Tablas principales:**
```
users
├── id (UUID, PK)
├── email (unique)
├── hashed_password
├── nombre
├── rol (enum: usuario, administrador)
├── is_active
├── created_at
└── updated_at

user_profiles
├── id (UUID, PK)
├── user_id (FK → users.id)
├── foto_url
├── etiquetas_interes (ARRAY)
├── localidad_preferida
├── disponibilidad_horaria
├── nivel_actividad
└── updated_at

activities
├── id (UUID, PK)
├── titulo
├── descripcion (TEXT)
├── tipo (enum: cultura, deporte, recreacion)
├── fecha_inicio
├── fecha_fin
├── ubicacion_direccion
├── ubicacion_coords (PostGIS POINT)
├── localidad (enum: chapinero, santa_fe, la_candelaria)
├── precio (DECIMAL)
├── es_gratis (BOOLEAN)
├── nivel_actividad (enum: bajo, medio, alto)
├── etiquetas (ARRAY)
├── contacto
├── enlace_externo
├── fuente_datos
├── estado (enum: activa, pendiente_validacion, inactiva)
├── popularidad_vistas (INT)
├── popularidad_favoritos (INT)
├── popularidad_normalizada (FLOAT)
├── created_at
└── updated_at

favorites
├── id (UUID, PK)
├── user_id (FK → users.id)
├── activity_id (FK → activities.id)
├── created_at
└── UNIQUE(user_id, activity_id)

refresh_tokens
├── id (UUID, PK)
├── user_id (FK → users.id)
├── token (TEXT, unique)
├── expires_at
├── is_revoked
└── created_at

etl_executions
├── id (UUID, PK)
├── fecha_inicio
├── fecha_fin
├── estado (enum: running, success, error)
├── total_procesados
├── total_exitosos
├── total_errores
├── logs (JSONB)
└── created_at

user_devices (IoT)
├── id (UUID, PK)
├── user_id (FK → users.id)
├── device_code (unique)
├── device_token
├── created_at
└── updated_at
```

**Índices Optimizados:**
- B-Tree: id (PK), email, fecha_inicio, estado, localidad, tipo
- GIN: etiquetas (array), full-text search (tsvector)
- GIST: ubicacion_coords (PostGIS spatial)

**Extensiones:**
- PostGIS (geolocalización)
- pg_trgm (búsqueda fuzzy)

---

#### Redis (Cache & Session Store)

**Base de datos en memoria**

**Usos:**
1. **Cache de recomendaciones**
   - Key: `recommendations:user:{user_id}`
   - TTL: 1 hora
   - Value: JSON con actividades recomendadas

2. **Rate limiting**
   - Key: `rate_limit:{endpoint}:{ip}`
   - TTL: 15 minutos
   - Value: contador de requests

3. **Cache de dashboard**
   - Key: `dashboard:metrics`
   - TTL: 5 minutos
   - Value: JSON con métricas agregadas

4. **Sessions temporales** (opcional)
   - Key: `session:{session_id}`
   - TTL: 30 minutos

---

### 3.4 Capa de Integración (ETL)

**Responsabilidad:** Importación automatizada de datos externos

**Tecnologías:**
- Python 3.11+
- Requests (HTTP client)
- Pandas (transformación)
- SQLAlchemy (carga)

**Estructura:**
```
etl/
├── src/
│   ├── extractors/
│   │   ├── idrd_extractor.py      # API IDRD
│   │   ├── csv_extractor.py       # CSV files
│   │   └── json_extractor.py      # JSON files
│   ├── transformers/
│   │   ├── activity_transformer.py # Normalización
│   │   └── deduplicator.py         # Detección duplicados
│   ├── loaders/
│   │   └── postgres_loader.py      # Inserción BD
│   ├── utils/
│   │   ├── logger.py
│   │   └── config.py
│   └── main.py                     # Orquestador ETL
├── data/                           # Datos temporales
└── Dockerfile                      # Container ETL
```

**Flujo ETL:**
```
1. EXTRACT
   ├── Conectar a fuente (API/CSV/JSON)
   ├── Obtener datos
   └── Validar respuesta

2. TRANSFORM
   ├── Normalizar formatos (fechas, coords, texto)
   ├── Validar campos obligatorios
   ├── Mapear a schema interno
   ├── Detectar duplicados
   └── Enriquecer datos

3. LOAD
   ├── Insertar en PostgreSQL
   ├── Estado: pendiente_validacion
   ├── Log de operaciones
   └── Actualizar etl_executions
```

---

## 4. Flujos de Datos Principales

### 4.1 Flujo de Autenticación

```
Usuario → Frontend → Backend → PostgreSQL → Redis → Backend → Frontend → Usuario
   │                  │            │           │         │         │
   │                  │            │           │         │         │
1. POST /auth/login   │            │           │         │         │
                      │            │           │         │         │
             2. Validar schema     │           │         │         │
                                   │           │         │         │
                      3. Query user (email)    │         │         │
                                               │         │         │
                      4. Verificar password    │         │         │
                                                         │         │
                      5. Generar JWT + Refresh Token     │         │
                                                         │         │
                      6. Guardar refresh token           │         │
                                                                   │
                      7. Return tokens (JSON)                      │
                                                                   │
                                              8. Almacenar en localStorage
```

### 4.2 Flujo de Búsqueda de Actividades

```
Usuario → Frontend → Backend → PostgreSQL → Redis → Backend → Frontend
   │                  │            │           │         │
   │                  │            │           │         │
1. GET /actividades?search=yoga&localidad=chapinero      │
                      │            │           │         │
             2. Validar params     │           │         │
                                   │           │         │
                      3. Check cache (opcional)          │
                                                          │
                      4. Query full-text search          │
                         + Filtros (localidad, tipo)     │
                         + Paginación                    │
                                                          │
                      5. Return resultados (JSON)        │
                                                          │
                                           6. Cache (opcional)
                                                          │
                      7. Return to frontend              │
                                                          │
                                              8. Render ActivityCards
```

### 4.3 Flujo de Recomendaciones IA

```
Usuario → Frontend → Backend → Redis → PostgreSQL → Backend → Frontend
                      │          │          │           │
                      │          │          │           │
1. GET /recomendaciones (Authenticated)     │           │
                      │          │          │           │
             2. Extract user_id (JWT)       │           │
                                │           │           │
                      3. Check cache        │           │
                         key: recommendations:user:123  │
                                            │           │
                      4. Si no existe, calcular:        │
                         - Get user profile             │
                         - Get user favorites           │
                         - Algoritmo híbrido            │
                         - Generate explanations        │
                                                         │
                      5. Cache results (1h)             │
                                                         │
                      6. Return recommendations         │
                                                         │
                                           7. Render recommendations
```

### 4.4 Flujo ETL Automatizado

```
Scheduler → ETL Service → Fuentes Externas → PostgreSQL → Backend Admin
    │            │               │                 │            │
    │            │               │                 │            │
1. Trigger (cron/manual)         │                 │            │
                 │               │                 │            │
        2. Start execution       │                 │            │
           (log: etl_executions) │                 │            │
                                 │                 │            │
        3. EXTRACT: GET API IDRD │                 │            │
                                 │                 │            │
        4. TRANSFORM: Normalize  │                 │            │
           Detect duplicates     │                 │            │
                                                   │            │
        5. LOAD: Insert activities (pendiente_validacion)       │
                                                                 │
        6. Update etl_executions (success/error)                │
                                                                 │
                                                    7. Admin valida
                                                       actividades
```

---

## 5. Seguridad

### 5.1 Capas de Seguridad

**1. Transporte:**
- HTTPS obligatorio en producción
- TLS 1.2+
- HSTS headers

**2. Autenticación:**
- OAuth2 Password Grant
- JWT (RS256) con claves asimétricas
- Access token: 30 min
- Refresh token: 30 días
- Token rotation

**3. Autorización:**
- Role-based access control (RBAC)
- Roles: usuario, administrador
- Protected routes en frontend
- Decorators en backend endpoints

**4. Datos:**
- Passwords: Bcrypt (cost factor 12)
- Datos sensibles: No almacenar en logs
- SQL injection: Prevención con ORM
- XSS: Sanitización en frontend
- CSRF: No aplica (API stateless)

**5. Rate Limiting:**
- Login: 5 intentos / 15 min
- APIs públicas: 100 req/min/IP
- Admin endpoints: 50 req/min/user

**6. Validación:**
- Input validation: Pydantic schemas
- Output sanitization
- File upload: Validación de tipo y tamaño

---

## 6. Escalabilidad y Performance

### 6.1 Estrategias de Performance

**Frontend:**
- Code splitting (lazy loading)
- Image lazy loading
- Minificación y compresión
- Service Worker (PWA)
- CDN para assets estáticos

**Backend:**
- Async/await (SQLAlchemy async)
- Connection pooling (PostgreSQL)
- Query optimization (índices)
- N+1 query prevention
- Pagination obligatoria

**Cache:**
- Redis para datos frecuentes
- Cache de recomendaciones (1h)
- Cache de dashboard (5 min)
- Cache de búsquedas populares

**Base de Datos:**
- Índices optimizados
- Partitioning (futuro, si >1M registros)
- Query análisis (EXPLAIN)
- Vacuum automático

### 6.2 Horizontal Scaling (Futuro)

```
                    Load Balancer
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Backend 1        Backend 2        Backend 3
        │                │                │
        └────────────────┼────────────────┘
                         │
                    PostgreSQL
                    (Primary)
                         │
                ┌────────┴────────┐
           Read Replica 1    Read Replica 2
```

---

## 7. Deployment y DevOps

### 7.1 Containerización (Docker)

**docker-compose.yml:**
```yaml
services:
  frontend:
    build: ./frontend
    ports: 3000:3000
    depends_on: backend
    
  backend:
    build: ./backend
    ports: 8000:8000
    depends_on: 
      - db
      - redis
    environment:
      - DATABASE_URL
      - REDIS_URL
      - JWT_SECRET_KEY
      
  db:
    image: postgres:15
    volumes: 
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=triqueta
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=secret
      
  redis:
    image: redis:7-alpine
    ports: 6379:6379
    
  nginx:
    image: nginx:alpine
    ports: 80:80, 443:443
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
      
  etl:
    build: ./etl
    depends_on: db
    # Cron schedule or manual trigger
```

### 7.2 CI/CD Pipeline (GitHub Actions)

```
┌─────────────┐
│  Git Push   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Lint     │  ← Ruff (Python), ESLint (TS)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Build     │  ← Docker images
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Test     │  ← Pytest, Vitest
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Security    │  ← Bandit, Semgrep, npm audit
│   Scan      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Deploy    │  ← Staging (auto)
│  (Staging)  │     Production (manual)
└─────────────┘
```

---

## 8. Monitoreo y Observabilidad

### 8.1 Logging

**Backend:**
- Logs estructurados (JSON)
- Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Contexto: request_id, user_id, timestamp
- Destino: stdout (Docker logs)

**Frontend:**
- Console logs (desarrollo)
- Error tracking (producción)
- Analytics events

### 8.2 Métricas

**Infraestructura:**
- Uptime monitoring
- CPU/Memory usage
- Disk I/O

**Aplicación:**
- Request rate
- Response time (P50, P90, P99)
- Error rate
- Cache hit ratio

**Negocio:**
- Usuarios activos
- Actividades vistas
- Búsquedas realizadas
- Favoritos guardados

---

## 9. Tecnologías y Versiones

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Frontend Framework | React | 18+ |
| Build Tool | Vite | 5+ |
| Language (Frontend) | TypeScript | 5+ |
| Styling | TailwindCSS | 3+ |
| UI Components | Shadcn UI | Latest |
| Routing | Tanstack Router | 1+ |
| State Management | React Query | 5+ |
| HTTP Client | Axios | 1+ |
| Backend Framework | FastAPI | 0.104+ |
| Language (Backend) | Python | 3.11+ |
| ORM | SQLAlchemy | 2.0+ |
| Validation | Pydantic | 2+ |
| Database | PostgreSQL | 15+ |
| Geo Extension | PostGIS | 3+ |
| Cache | Redis | 7+ |
| Reverse Proxy | Nginx | 1.24+ |
| Container Runtime | Docker | 24+ |
| Orchestration | Docker Compose | 2+ |
| CI/CD | GitHub Actions | - |

---

## 10. Consideraciones Especiales

### 10.1 Dispositivos IoT

**Arquitectura de Comunicación:**
```
Dispositivo IoT → API Backend → PostgreSQL
       │              │              │
       │              │              │
   1. Autenticación   │              │
      (device_token)  │              │
                      │              │
           2. GET /api/v1/iot/recommendations
                                     │
                      3. Query user_id del device
                                     │
                      4. Generate recommendations
                                     │
           5. Return top 3-5 (optimizado para display)
```

**Protocolo:**
- HTTP/REST (simple para MVP)
- Futuro: MQTT o WebSocket

### 10.2 Accesibilidad

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader compatible
- WCAG 2.1 Level AA

### 10.3 Internacionalización (Futuro)

- i18n ready (estructura preparada)
- Español por defecto
- Inglés (futuro)

---

**Versión:** 1.0  
**Última actualización:** 22 de Octubre de 2025  
**Estado:** ✅ Aprobado para implementación
