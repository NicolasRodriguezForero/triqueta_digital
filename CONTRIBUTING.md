# Guía de Contribución - Triqueta Digital

## 🎯 Introducción

¡Gracias por tu interés en contribuir a Triqueta Digital! Esta guía te ayudará a entender cómo trabajamos y cómo puedes hacer contribuciones efectivas.

## 🔧 Configuración del Entorno

### Prerrequisitos
- Docker y Docker Compose
- Git
- Node.js 18+ (para desarrollo frontend local)
- Python 3.11+ (para desarrollo backend local)

### Setup Inicial
1. Fork el repositorio
2. Clona tu fork localmente
3. Configura el upstream: `git remote add upstream <url-repo-original>`
4. Sigue las instrucciones del README.md para levantar el proyecto

## 🌿 Workflow de Git

### Branches
- `main`: Código en producción (protegido)
- `develop`: Integración de features (protegido)
- `feature/*`: Nuevas funcionalidades
- `fix/*`: Corrección de bugs
- `refactor/*`: Refactorización de código
- `docs/*`: Cambios en documentación

### Proceso de Contribución

1. **Sincroniza tu fork:**
   ```bash
   git checkout develop
   git pull upstream develop
   ```

2. **Crea un branch:**
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```

3. **Haz tus cambios:**
   - Escribe código limpio y bien documentado
   - Sigue las convenciones del proyecto
   - Añade tests cuando sea apropiado

4. **Commit:**
   ```bash
   git add .
   git commit -m "feat: descripción del cambio"
   ```

5. **Push:**
   ```bash
   git push origin feature/nombre-descriptivo
   ```

6. **Crea un Pull Request:**
   - Describe los cambios claramente
   - Referencia issues relacionados
   - Asegúrate de que pasen los tests de CI

## 📝 Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formateo, punto y coma faltante, etc.
- `refactor:` Refactorización de código
- `test:` Añadir tests
- `chore:` Tareas de mantenimiento

**Ejemplos:**
```
feat: implementar dashboard administrativo
fix: corregir error en cálculo de recomendaciones
docs: actualizar README con instrucciones de ETL
refactor: simplificar lógica de autenticación
```

## 🎨 Estándares de Código

### Backend (Python)
- **PEP 8:** Guía de estilo oficial de Python
- **Type Hints:** Obligatorios en todas las funciones
- **Docstrings:** Formato Google-style
- **Linting:** Ruff (configurado en `ruff.toml`)

**Ejemplo:**
```python
async def get_user_by_email(email: str, db: AsyncSession) -> Usuario | None:
    """
    Retrieve user by email address.
    
    Args:
        email: User's email address
        db: Database session
        
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(
        select(Usuario).filter(Usuario.email == email)
    )
    return result.scalar_one_or_none()
```

### Frontend (TypeScript/React)
- **ESLint:** Strict configuration
- **Functional Components:** Preferir sobre class components
- **Hooks:** Usar custom hooks para lógica reutilizable
- **Type Safety:** TypeScript strict mode habilitado

**Ejemplo:**
```typescript
interface UserProfileProps {
  userId: number;
}

export function UserProfile({ userId }: UserProfileProps) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => getUserById(userId),
  });

  if (isLoading) return <LoadingSpinner />;
  if (!user) return <NotFound />;

  return <div>...</div>;
}
```

## 🧪 Testing

### Backend Tests
```bash
# Ejecutar todos los tests
docker compose exec backend pytest

# Tests con coverage
docker compose exec backend pytest --cov=app --cov-report=html

# Tests específicos
docker compose exec backend pytest tests/test_auth.py
```

### Frontend Tests
```bash
cd frontend
npm test
```

**Cobertura mínima esperada:** 70%

## 🔍 Code Review

### Checklist del PR
- [ ] El código sigue las convenciones del proyecto
- [ ] Los tests pasan localmente
- [ ] Se añadieron tests para nuevo código
- [ ] La documentación está actualizada
- [ ] No hay warnings de linter
- [ ] El PR tiene una descripción clara

### Proceso de Review
1. Al menos 1 aprobación requerida
2. CI debe pasar (tests, linting)
3. Sin conflictos con branch base
4. Commits squashed si hay múltiples pequeños

## 🐛 Reportar Bugs

### Template de Issue
```markdown
**Descripción:**
Breve descripción del bug

**Pasos para Reproducir:**
1. Ir a '...'
2. Click en '...'
3. Ver error

**Comportamiento Esperado:**
Qué debería suceder

**Comportamiento Actual:**
Qué está sucediendo

**Entorno:**
- OS: [Ubuntu 22.04]
- Browser: [Chrome 120]
- Versión: [commit hash]
```

## 💡 Solicitar Features

### Template de Feature Request
```markdown
**Problema:**
Descripción del problema que esta feature resuelve

**Solución Propuesta:**
Cómo debería funcionar

**Alternativas Consideradas:**
Otras opciones que consideraste

**Contexto Adicional:**
Screenshots, mockups, etc.
```

## 📚 Documentación

- Mantén el README.md actualizado
- Documenta funciones complejas
- Añade comentarios cuando el código no es auto-explicativo
- Actualiza los docstrings de API

## 🏗️ Arquitectura

### Principios
- **SOLID:** Especialmente Single Responsibility
- **DRY:** Don't Repeat Yourself
- **KISS:** Keep It Simple, Stupid
- **YAGNI:** You Aren't Gonna Need It

### Estructura de Código
```
backend/
  app/
    api/      # Endpoints
    core/     # Config, dependencies
    models/   # SQLAlchemy models
    schemas/  # Pydantic schemas
    services/ # Business logic
    utils/    # Helpers

frontend/
  src/
    components/  # Reusable UI
    pages/       # Route components
    services/    # API calls
    hooks/       # Custom hooks
    utils/       # Helpers
```

## 🙏 Reconocimientos

Todas las contribuciones son valoradas y reconocidas. Los contribuidores top aparecerán en el README principal.

## 📞 Contacto

¿Preguntas? Abre una issue con la etiqueta `question`.

---

**¡Gracias por contribuir a Triqueta Digital! 🚀**
