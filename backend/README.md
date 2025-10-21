# Triqueta Digital - Backend API

FastAPI backend para Triqueta Digital.

## Stack Tecnológico

- **Framework:** FastAPI 0.104+
- **Python:** 3.11+
- **Database:** PostgreSQL 15+ (async con asyncpg)
- **ORM:** SQLAlchemy 2.0+ (async)
- **Migrations:** Alembic
- **Cache:** Redis
- **Authentication:** OAuth2 + JWT
- **Testing:** pytest + pytest-asyncio

## Instalación Local

### Prerrequisitos
- Python 3.11+
- PostgreSQL 15+
- Redis

### Setup

1. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

2. **Instalar dependencias:**
```bash
pip install -r requirements-dev.txt
```

3. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

4. **Inicializar base de datos:**
```bash
alembic upgrade head
```

5. **Ejecutar servidor:**
```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://localhost:8000`

## Uso con Docker

```bash
# Desde el directorio raíz del proyecto
docker-compose up backend
```

## Documentación API

Una vez el servidor esté corriendo:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Tests

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_auth.py
```

## Estructura del Proyecto

```
backend/
├── app/
│   ├── api/v1/          # Routers (endpoints)
│   ├── core/            # Config, security
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── db/              # Database config
│   ├── middleware/      # Custom middleware
│   └── utils/           # Utilities
├── alembic/             # Database migrations
├── tests/               # Tests
└── main.py              # Entry point
```

## Desarrollo

### Crear nueva migración
```bash
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

### Linting y formateo
```bash
ruff check .
ruff format .
```

### Type checking
```bash
mypy app
```

## Variables de Entorno

Ver `.env.example` para todas las variables disponibles.

Variables críticas:
- `DATABASE_URL`: URL de PostgreSQL
- `REDIS_URL`: URL de Redis
- `SECRET_KEY`: Clave secreta para JWT

## Estado del Desarrollo

Ver `PLAN_IMPLEMENTACION.md` en la raíz del proyecto para el estado actual.
