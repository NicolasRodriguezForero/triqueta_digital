# Triqueta Digital

Plataforma digital que conecta actividades culturales, recreativas y deportivas en las localidades de Chapinero, Santa Fe y La Candelaria (Bogotá, Colombia).

## 🎯 Visión General

Triqueta Digital centraliza la información dispersa de la oferta cultural y deportiva local, facilitando a los ciudadanos el descubrimiento y participación en actividades mediante recomendaciones personalizadas con inteligencia artificial.

**Objetivos principales:**
- ✅ Integrar al menos 70% de la oferta cultural y deportiva disponible
- ✅ Proveer recomendaciones personalizadas mediante IA
- ✅ Facilitar participación ciudadana en actividades locales
- ✅ MVP con 200+ usuarios activos mensuales

## 🏗️ Arquitectura

**SOA Modular** - Monolito modular con servicios internos bien definidos.

```
┌─────────────────┐
│     Nginx       │  Reverse Proxy
│   (Port 80)     │  
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌──▼──────┐
│Frontend│  │ Backend │  FastAPI + Python 3.11+
│  Vite  │  │ (API)   │  SQLAlchemy + Pydantic
│  React │  │ :8000   │
│ :5173  │  └────┬────┘
└────────┘       │
            ┌────┴────┐
            │         │
      ┌─────▼───┐ ┌──▼─────┐
      │PostgreSQL│ │ Redis  │
      │  :5432   │ │ :6379  │
      └──────────┘ └────────┘
```

## 🚀 Quick Start

### Prerrequisitos
- Docker y Docker Compose
- Git

### Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd proyecto
```

2. **Configurar variables de entorno:**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Editar los archivos .env según sea necesario
```

3. **Levantar servicios con Docker:**
```bash
docker-compose up -d
```

4. **Inicializar base de datos:**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Acceder a la aplicación:**
- **Aplicación principal:** http://localhost (puerto 80)
- **Frontend:** http://localhost/
- **Backend API:** http://localhost/api/v1/
- **API Docs (Swagger):** http://localhost/docs
- **API Docs (ReDoc):** http://localhost/redoc
- **Health Check:** http://localhost/health
- **PostgreSQL:** localhost:5432 (para herramientas externas)
- **Redis:** localhost:6379 (para herramientas externas)

## 📚 Documentación

### Documentación Técnica
- **[SRS - Software Requirements Specification](./docs/README.md)** - Requisitos completos
- **[Plan de Implementación](./PLAN_IMPLEMENTACION.md)** - Roadmap de desarrollo
- **[Backend README](./backend/README.md)** - Documentación del backend
- **[Frontend README](./frontend/README.md)** - Documentación del frontend

### Estándares y Normativas
- ISO/IEC/IEEE 29148:2018 - Requirements Engineering
- ISO/IEC 25010:2023 - Software Quality Model
- OWASP ASVS v5.0 Nivel 2 - Security Verification
- WCAG 2.1 Level AA - Accessibility
- Ley 1581/2012 - Protección de Datos (Colombia)

## 🛠️ Stack Tecnológico

### Frontend
- React 18+ + Vite
- TypeScript
- TailwindCSS + Shadcn UI
- Tanstack Router + React Query
- Axios

### Backend
- Python 3.11+ + FastAPI
- SQLAlchemy 2.0+ (async)
- Pydantic
- OAuth2 + JWT
- Redis

### Base de Datos
- PostgreSQL 15+
- PostGIS (geolocalización)

### Infraestructura
- Docker + Docker Compose
- GitHub Actions (CI/CD)

## 📊 Estado del Desarrollo

**Progreso:** 10% (Setup inicial) ⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜

### Sprint Actual: Sprint 1 - Setup + Autenticación
**Duración:** Semanas 1-2  
**Estado:** 🟡 En progreso

Ver [PLAN_IMPLEMENTACION.md](./PLAN_IMPLEMENTACION.md) para detalles completos.

### Próximos Sprints
- **Sprint 2:** Actividades + Búsqueda (Semanas 3-4)
- **Sprint 3:** Favoritos + Recomendaciones IA (Semanas 5-6)
- **Sprint 4:** Admin + ETL (Semanas 7-8)

## 🧪 Testing

### Backend
```bash
# Instalar dependencias de desarrollo
pip install -r backend/requirements-dev.txt

# Ejecutar tests
pytest

# Con coverage
pytest --cov=app --cov-report=html
```

### Frontend
```bash
# Ejecutar tests
npm run test

# Con coverage
npm run test:coverage
```

## 🔧 Desarrollo Local (Sin Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📝 Scripts Útiles

### Base de Datos
```bash
# Crear nueva migración
docker-compose exec backend alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
docker-compose exec backend alembic upgrade head

# Revertir migración
docker-compose exec backend alembic downgrade -1
```

### Linting y Formateo
```bash
# Backend
cd backend
ruff check .
ruff format .

# Frontend
cd frontend
npm run lint
npm run format
```

## 🤝 Contribución

### Workflow de Git
1. Crear branch desde `develop`: `git checkout -b feature/nombre`
2. Hacer commits descriptivos
3. Push y crear Pull Request
4. Code review requerido
5. Merge a `develop`

### Convenciones
- **Commits:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- **Branches:** `feature/nombre`, `fix/nombre`, `refactor/nombre`
- **Python:** PEP 8, type hints obligatorios
- **TypeScript:** ESLint strict, functional components

## 📄 Licencia

Proyecto académico - Universidad Santo Tomás  
Diseño Creativo - 8vo Semestre  
Octubre 2025

## 👥 Equipo

Ver documentación del proyecto para información del equipo.

## 🔗 Enlaces Útiles

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [TailwindCSS Docs](https://tailwindcss.com/)
- [Shadcn UI](https://ui.shadcn.com/)
- [Tanstack Router](https://tanstack.com/router)
- [Tanstack Query](https://tanstack.com/query)

## 🐛 Reporte de Issues

Para reportar bugs o solicitar features, crear un issue en el repositorio con:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots (si aplica)

## 📞 Soporte

Para preguntas sobre el proyecto, consultar la documentación en `/docs` o contactar al equipo de desarrollo.

---

**¿Listo para desarrollar?**  
Ver [PLAN_IMPLEMENTACION.md](./PLAN_IMPLEMENTACION.md) para comenzar con el Sprint 1.
