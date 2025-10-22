# Base de Datos - Triqueta Digital

Scripts SQL para PostgreSQL 15+

---

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `schema.sql` | Script completo de creación de tablas, índices y constraints |
| `seed.sql` | Datos de prueba para desarrollo |

---

## Instalación

### Requisitos

- PostgreSQL 15+
- Extensiones: `pgcrypto`, `postgis` (opcional)

### 1. Crear Base de Datos

```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE triqueta_digital;

# Conectar a la base de datos
\c triqueta_digital
```

### 2. Ejecutar Script de Esquema

```bash
# Desde la terminal
psql -U postgres -d triqueta_digital -f schema.sql

# O desde psql
\i /ruta/absoluta/schema.sql
```

### 3. Cargar Datos de Prueba (Opcional)

```bash
psql -U postgres -d triqueta_digital -f seed.sql
```

---

## Estructura de Tablas

### Tablas Core (MVP)

1. **usuarios** - Cuentas de usuarios
2. **perfiles_usuarios** - Preferencias de usuarios
3. **actividades** - Catálogo de actividades
4. **favoritos** - Relación usuarios-actividades
5. **refresh_tokens** - Tokens de autenticación
6. **etl_executions** - Logs ETL

### Tablas Post-MVP

7. **dispositivos** - Dispositivos IoT
8. **usuarios_dispositivos** - Vinculación IoT

---

## Usuarios de Prueba

### Ciudadanos

| Email | Password | Rol | Intereses |
|-------|----------|-----|-----------|
| maria.rodriguez@example.com | password123 | usuario | Arte, Música, Teatro |
| carlos.gonzalez@example.com | password123 | usuario | Deporte, Ciclismo |
| lucia.martinez@example.com | password123 | usuario | Cultura, Cine |

### Administrador

| Email | Password | Rol |
|-------|----------|-----|
| admin@triqueta.com | password123 | administrador |

> ⚠️ **IMPORTANTE**: Estos passwords son SOLO para desarrollo. Cambiar en producción.

---

## Actividades de Prueba

El script `seed.sql` crea:
- ✅ 6 actividades activas (2 por localidad)
- 🟡 1 actividad pendiente de validación
- 📍 Localidades: Chapinero, Santa Fe, La Candelaria
- 🏷️ Tipos: Cultura, Deporte, Recreación

---

## Comandos Útiles

### Verificar Tablas

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

### Ver Estructura de una Tabla

```sql
\d+ usuarios
```

### Listar Índices

```sql
SELECT 
    tablename, 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename, indexname;
```

### Contar Registros

```sql
SELECT 
    'usuarios' AS tabla, COUNT(*) AS total FROM usuarios
UNION ALL
    SELECT 'actividades', COUNT(*) FROM actividades
UNION ALL
    SELECT 'favoritos', COUNT(*) FROM favoritos;
```

### Borrar Todos los Datos (CUIDADO)

```sql
TRUNCATE TABLE 
    usuarios_dispositivos, 
    dispositivos, 
    favoritos, 
    refresh_tokens, 
    etl_executions, 
    actividades, 
    perfiles_usuarios, 
    usuarios 
CASCADE;
```

---

## Backup y Restore

### Crear Backup

```bash
# Backup completo
pg_dump -U postgres -d triqueta_digital -F c -f backup_triqueta.dump

# Solo esquema
pg_dump -U postgres -d triqueta_digital --schema-only -f schema_backup.sql

# Solo datos
pg_dump -U postgres -d triqueta_digital --data-only -f data_backup.sql
```

### Restaurar Backup

```bash
# Desde dump
pg_restore -U postgres -d triqueta_digital backup_triqueta.dump

# Desde SQL
psql -U postgres -d triqueta_digital -f schema_backup.sql
```

---

## Migraciones Futuras

Para cambios en el esquema, crear archivos de migración:

```
database/migrations/
├── 001_initial_schema.sql
├── 002_add_new_table.sql
└── 003_alter_column.sql
```

---

## Conexión desde la Aplicación

### Variables de Entorno

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/triqueta_digital
DB_HOST=localhost
DB_PORT=5432
DB_NAME=triqueta_digital
DB_USER=usuario
DB_PASSWORD=password
```

### Python (SQLAlchemy)

```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://usuario:password@localhost:5432/triqueta_digital"
engine = create_engine(DATABASE_URL)
```

---

## Troubleshooting

### Error: "extension pgcrypto does not exist"

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### Error: "permission denied"

```sql
GRANT ALL PRIVILEGES ON DATABASE triqueta_digital TO usuario;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO usuario;
```

### Resetear Secuencias

```sql
SELECT setval('tabla_id_seq', (SELECT MAX(id) FROM tabla));
```

---

## Referencias

- Documentación: `docs/Modelo_Relacional_Triqueta.md`
- SRS: `docs/SRS_Arquitectura_y_Datos.md`
- PostgreSQL Docs: https://www.postgresql.org/docs/15/
