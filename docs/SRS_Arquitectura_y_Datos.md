# Arquitectura del Sistema y Modelo de Datos - Triqueta Digital

## 5. Arquitectura del Sistema

### 5.1 Estilo Arquitectónico: SOA Modular

**Arquitectura Orientada a Servicios (SOA)** implementada como monolito modular en FastAPI.

**Ventajas:**
- ✅ Simplicidad operacional
- ✅ Desarrollo rápido
- ✅ Transacciones ACID nativas
- ✅ Menor latencia
- ✅ Facilidad debugging
- ✅ Preparado para microservicios futuros

---

### 5.2 Stack Tecnológico

**Frontend:**
- React 18+ + Vite + TypeScript
- TailwindCSS + Shadcn UI
- Tanstack Router + Tanstack React Query
- Axios para HTTP client

**Backend:**
- Python 3.11+ + FastAPI
- SQLAlchemy 2.0+ (ORM async)
- Pydantic (validación)
- JWT + OAuth2
- Redis (caché, rate limiting)

**Base de Datos:**
- PostgreSQL 15+
- PostGIS (coordenadas GPS)

**Infraestructura:**
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- Nginx (reverse proxy)

---

### 5.3 Estructura del Backend (FastAPI)

```
backend/app/
├── main.py                    # Entry point
├── core/                      # Config, security
│   ├── config.py              # Settings
│   ├── security.py            # JWT, OAuth2
│   └── dependencies.py
├── api/v1/                    # Routers
│   ├── auth.py
│   ├── users.py
│   ├── activities.py
│   ├── recommendations.py     # IA Module
│   ├── favorites.py
│   ├── admin.py
│   └── iot.py
├── models/                    # SQLAlchemy models
├── schemas/                   # Pydantic DTOs
├── services/                  # Business logic
│   ├── auth_service.py
│   ├── activity_service.py
│   ├── recommendation_service.py  # ⭐ Módulo IA
│   └── ...
├── db/                        # Database
└── tests/
```

---

### 5.4 Módulo de IA (Recomendaciones)

**Ubicación:** `backend/app/services/recommendation_service.py`

**Algoritmo MVP:**
```python
def calcular_score(actividad, usuario):
    score = actividad.popularidad_normalizada * 100
    
    # Bonus por etiquetas
    coincidencias = set(usuario.etiquetas) & set(actividad.etiquetas)
    score += len(coincidencias) * 10
    
    # Bonus por localidad
    if actividad.localidad == usuario.localidad_preferida:
        score += 5
    
    return score
```

---

## 6. Interfaces Externas

### 6.1 API REST

**Base URL:** `https://api.triqueta.com/api/v1`

**Endpoints principales:**
- `POST /auth/register` - Registro
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token
- `GET /actividades` - Listar actividades
- `GET /actividades/{id}` - Detalle
- `GET /recomendaciones` - Recomendaciones personalizadas
- `POST /favoritos` - Guardar favorito
- `GET /admin/dashboard` - Dashboard admin

**Documentación:** Swagger en `/docs`

---

## 7. Modelo de Datos

### 7.1 PostgreSQL - Tablas Principales

#### `usuarios`
```sql
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    foto_url VARCHAR(500),
    rol VARCHAR(50) DEFAULT 'usuario',
    estado VARCHAR(50) DEFAULT 'activo',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `perfiles_usuarios`
```sql
CREATE TABLE perfiles_usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    etiquetas_interes TEXT[],
    localidad_preferida VARCHAR(100),
    disponibilidad_horaria JSONB,
    nivel_actividad_preferido VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `actividades`
```sql
CREATE TABLE actividades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    fecha_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    fecha_fin TIMESTAMP WITH TIME ZONE,
    ubicacion_direccion VARCHAR(500) NOT NULL,
    ubicacion_lat DECIMAL(10, 8) NOT NULL,
    ubicacion_lng DECIMAL(11, 8) NOT NULL,
    localidad VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) DEFAULT 0,
    es_gratis BOOLEAN DEFAULT TRUE,
    nivel_actividad VARCHAR(50),
    etiquetas TEXT[] NOT NULL,
    contacto VARCHAR(255),
    enlace_externo VARCHAR(500),
    fuente VARCHAR(100) DEFAULT 'manual',
    estado VARCHAR(50) DEFAULT 'activa',
    popularidad_favoritos INTEGER DEFAULT 0,
    popularidad_vistas DECIMAL(10, 2) DEFAULT 0,
    popularidad_normalizada DECIMAL(5, 4) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_actividades_localidad ON actividades(localidad);
CREATE INDEX idx_actividades_tipo ON actividades(tipo);
CREATE INDEX idx_actividades_fecha_inicio ON actividades(fecha_inicio);
CREATE INDEX idx_actividades_estado ON actividades(estado);
CREATE INDEX idx_actividades_etiquetas ON actividades USING GIN(etiquetas);
```

#### `favoritos`
```sql
CREATE TABLE favoritos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    actividad_id UUID REFERENCES actividades(id) ON DELETE CASCADE,
    fecha_guardado TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, actividad_id)
);

CREATE INDEX idx_favoritos_user_id ON favoritos(user_id);
CREATE INDEX idx_favoritos_actividad_id ON favoritos(actividad_id);
```

#### `refresh_tokens`
```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token_hash ON refresh_tokens(token_hash);
```

#### `dispositivos` (Post-MVP)
```sql
CREATE TABLE dispositivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(50) DEFAULT 'cubo',
    estado VARCHAR(50) DEFAULT 'disponible',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE usuarios_dispositivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    device_id UUID REFERENCES dispositivos(id) ON DELETE CASCADE,
    device_token TEXT,
    vinculado_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    desvinculado_at TIMESTAMP WITH TIME ZONE
);
```

#### `etl_executions`
```sql
CREATE TABLE etl_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    estado VARCHAR(50) DEFAULT 'corriendo',
    actividades_procesadas INTEGER DEFAULT 0,
    actividades_exitosas INTEGER DEFAULT 0,
    actividades_errores INTEGER DEFAULT 0,
    error_log TEXT,
    triggered_by UUID REFERENCES usuarios(id)
);
```

---

### 7.2 Ventajas de PostgreSQL para este Proyecto

**1. Relaciones Estructuradas**
- ✅ Modelo relacional claro (usuarios-actividades-favoritos)
- ✅ Integridad referencial (foreign keys)
- ✅ Transacciones ACID

**2. Flexibilidad con JSONB**
- ✅ Campos semiestructurados (disponibilidad_horaria)
- ✅ Queries eficientes en JSON
- ✅ Índices en campos JSONB

**3. Búsqueda Full-Text**
- ✅ Búsqueda nativa en PostgreSQL
- ✅ Pesos de relevancia
- ✅ Búsqueda multiidioma (español)

**4. Arrays Nativos**
- ✅ Almacenar etiquetas como array
- ✅ Operaciones de conjuntos (intersección)
- ✅ Índices GIN para arrays

**5. PostGIS para Geolocalización**
- ✅ Extensión para coordenadas GPS
- ✅ Búsquedas por proximidad
- ✅ Cálculo de distancias

**6. Madurez y Ecosistema**
- ✅ Amplia adopción
- ✅ Excelente documentación
- ✅ Integración con SQLAlchemy

**7. Escalabilidad**
- ✅ Replicas de lectura
- ✅ Particionamiento de tablas
- ✅ Connection pooling

---

## 8. Restricciones de Diseño

### 8.1 Arquitectónicas
- Backend: Único proyecto FastAPI modular
- Frontend: SPA con React + Vite
- ETL: Script Docker separado
- Base de datos: PostgreSQL compartida

### 8.2 Tecnológicas
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker Engine 20+

### 8.3 De Seguridad
- HTTPS obligatorio en producción
- JWT con RS256
- Passwords con bcrypt (cost 12+)
- Rate limiting habilitado

---

## 9. Apéndices

### 9.1 Glosario Técnico

| Término | Descripción |
|---------|-------------|
| **SOA** | Service-Oriented Architecture |
| **JWT** | JSON Web Token para autenticación |
| **ORM** | Object-Relational Mapping (SQLAlchemy) |
| **ETL** | Extract, Transform, Load |
| **CRUD** | Create, Read, Update, Delete |
| **DTO** | Data Transfer Object (Pydantic schemas) |

### 9.2 Convenciones de Código

**Python:**
- PEP 8
- Type hints obligatorios
- Docstrings en funciones públicas

**TypeScript:**
- ESLint + Prettier
- Interfaces para types
- Functional components

**Git:**
- Commits en español o inglés consistente
- Conventional Commits
- Branch naming: `feature/nombre`, `fix/nombre`

---

## Resumen de Decisiones Arquitectónicas

| Decisión | Justificación |
|----------|---------------|
| **SOA Modular (Monolito)** | Simplicidad para MVP, escalable a futuro |
| **PostgreSQL** | Relacional + flexible (JSONB, arrays, PostGIS) |
| **FastAPI** | Alto rendimiento, async, type-safe, OpenAPI |
| **React + Vite** | Ecosistema maduro, dev experience, rendimiento |
| **Docker** | Portabilidad, consistencia dev-prod |
| **ETL Separado** | Desacoplamiento, ejecuciones independientes |
| **JWT** | Stateless, escalable, estándar industria |

---

**Fin del documento SRS - Arquitectura y Datos**
