# Tests - Triqueta Digital Backend

## 📋 Estructura de Tests

```
tests/
├── conftest.py           # Fixtures y configuración de pytest
├── test_auth.py          # Tests de autenticación (registro, login, tokens)
└── test_users.py         # Tests de perfil de usuario
```

## 🚀 Ejecutar Tests

### Requisito previo: Crear BD de tests

```bash
# Solo la primera vez
docker compose exec db psql -U triqueta_user -d triqueta_db -c "CREATE DATABASE triqueta_test;"
```

### Desde el contenedor Docker (recomendado)

```bash
docker compose exec backend pytest
```

### Desde el host (requiere dependencias instaladas)

```bash
cd backend
pytest
```

### Con coverage

```bash
# Desde el host
pytest --cov=app --cov-report=html

# Desde el contenedor
docker compose exec backend pytest --cov=app --cov-report=html
```

El reporte HTML se generará en `htmlcov/index.html`.

## ⚙️ Configuración

Los tests utilizan una base de datos PostgreSQL separada (`triqueta_test`) definida en `conftest.py`.

**Importante:** Los tests crean y destruyen tablas antes y después de cada test para garantizar aislamiento.

## 📝 Tests Implementados

### Authentication (`test_auth.py`)

- ✅ Registro exitoso de usuario
- ✅ Registro con email duplicado (falla)
- ✅ Registro con contraseña débil (falla)
- ✅ Login exitoso
- ✅ Login con contraseña incorrecta (falla)
- ✅ Login con usuario inexistente (falla)
- ✅ Obtener usuario actual con token válido
- ✅ Obtener usuario sin token (falla)
- ✅ Refresh token exitoso
- ✅ Logout y revocación de refresh token
- ✅ OAuth2 password flow (form-based login)

### User Profile (`test_users.py`)

- ✅ Obtener perfil de usuario
- ✅ Obtener perfil sin autenticación (falla)
- ✅ Actualizar perfil completo
- ✅ Actualizar etiquetas de interés
- ✅ Actualizar disponibilidad y nivel de actividad
- ✅ Actualización parcial de perfil
- ✅ Eliminar cuenta (soft delete)
- ✅ Obtener usuario por ID
- ✅ Actualizar perfil sin autenticación (falla)

## 🎯 Coverage Objetivo

- **Target:** >80% de cobertura en backend
- **Módulos críticos:** `services/`, `api/`, `core/dependencies`

## 📌 Notas

- Los tests usan `pytest-asyncio` para pruebas asíncronas
- `httpx.AsyncClient` simula requests HTTP al API
- Los fixtures en `conftest.py` crean y limpian la BD automáticamente
- **Rate limiting está deshabilitado** en tests vía `.env.test` (`RATE_LIMIT_ENABLED=False`)
- Los tests cargan configuración desde `.env.test` automáticamente

## 🔧 Troubleshooting

### Error: "database does not exist"

Crear la base de datos de tests manualmente:

```bash
docker compose exec db psql -U triqueta_user -c "CREATE DATABASE triqueta_test;"
```

### Tests fallan por columnas ARRAY

Asegurarse de usar PostgreSQL en vez de SQLite (ya configurado en `conftest.py`).
