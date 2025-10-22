# Requisitos No Funcionales - Triqueta Digital
## Basado en ISO/IEC 25010:2023

## 4. Requisitos No Funcionales

### 4.1 Usabilidad

#### RNF-001: Accesibilidad
**Estándar:** WCAG 2.1 Level AA

**Requisitos específicos:**
- Contraste de colores mínimo 4.5:1 para texto normal
- Contraste de colores mínimo 3:1 para texto grande (18pt+)
- Navegación completa por teclado (tab, enter, esc, flechas)
- Textos alternativos (alt) en todas las imágenes significativas
- Labels asociados a todos los inputs de formularios
- Orden lógico de foco (tab order)
- Indicadores visuales de foco
- No uso de color como único medio de transmitir información
- Subtítulos en videos (si aplica)

**Herramientas de validación:**
- axe DevTools
- WAVE
- Lighthouse accessibility audit

**Métrica de aceptación:**
- Score de accesibilidad Lighthouse >= 95
- 0 errores críticos en WAVE

---

#### RNF-002: Aprendizaje y Usabilidad
**Descripción:** La interfaz debe ser intuitiva y fácil de aprender.

**Requisitos:**
- Usuario nuevo debe poder buscar actividades en <5 minutos sin instrucciones
- Formularios con validación inline y mensajes de error claros
- Máximo 3 clics para acciones principales
- Feedback visual inmediato en todas las acciones (loading, success, error)
- Tooltips en funciones no evidentes
- Mensajes de error en lenguaje claro (no códigos técnicos)

**Métricas de aceptación:**
- System Usability Scale (SUS) score >70
- Tasa de abandono en registro <30%
- Tasa de completitud en onboarding >80%

---

#### RNF-003: Diseño Responsive
**Descripción:** La interfaz debe adaptarse a diferentes tamaños de pantalla.

**Breakpoints:**
- Mobile: 375px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px - 1920px
- Large Desktop: 1921px+

**Requisitos:**
- Diseño mobile-first
- Touch targets mínimo 44x44px en móvil
- No scroll horizontal
- Imágenes responsive con lazy loading
- Tipografía escalable (rem/em)

**Criterios de aceptación:**
- 100% funcionalidad en todos los breakpoints
- Lighthouse Mobile score >90

---

### 4.2 Eficiencia de Desempeño

#### RNF-004: Tiempo de Respuesta API
**Descripción:** La API debe responder rápidamente a las peticiones.

**Objetivos:**
- P50 (mediana): <500ms
- P90: <2s
- P95: <3s
- P99: <5s

**Por tipo de endpoint:**
| Tipo | P90 Target |
|------|-----------|
| Autenticación | <1s |
| Listados con paginación | <2s |
| Búsqueda | <2s |
| Detalle de actividad | <500ms |
| Recomendaciones | <1s |
| Operaciones CRUD | <1s |

**Herramientas de medición:**
- Prometheus + Grafana
- APM (Application Performance Monitoring)
- Logs de latencia

**Criterios de aceptación:**
- 90% de requests cumplen targets
- No timeout errors bajo carga normal

---

#### RNF-005: Tiempo de Carga Frontend
**Descripción:** La aplicación web debe cargar rápidamente.

**Métricas Core Web Vitals:**
- **LCP (Largest Contentful Paint):** <2.5s
- **FID (First Input Delay):** <100ms
- **CLS (Cumulative Layout Shift):** <0.1

**Métricas adicionales:**
- **FCP (First Contentful Paint):** <1.8s
- **TTI (Time to Interactive):** <3.8s
- **Speed Index:** <3.4s

**Optimizaciones requeridas:**
- Code splitting por rutas
- Lazy loading de componentes pesados
- Lazy loading de imágenes
- Compresión gzip/brotli
- Minificación de JS/CSS
- Caché de assets estáticos (1 año)
- CDN para assets estáticos

**Criterios de aceptación:**
- Lighthouse Performance score >90 (desktop)
- Lighthouse Performance score >80 (mobile)

---

#### RNF-006: Capacidad y Escalabilidad
**Descripción:** El sistema debe soportar la carga esperada y poder escalar.

**Capacidad mínima MVP:**
- 200 usuarios concurrentes
- 1,000 actividades en catálogo
- 100 requests/segundo
- 10,000 usuarios registrados

**Escalabilidad:**
- Arquitectura stateless (horizontal scaling)
- Base de datos con replicas de lectura
- Caché distribuida (Redis)
- Load balancer

**Criterios de aceptación:**
- Tests de carga con 300 usuarios concurrentes sin degradación
- CPU usage <70% bajo carga normal
- Memory usage <80% bajo carga normal

---

#### RNF-007: Optimización de Consultas
**Descripción:** Las consultas a base de datos deben estar optimizadas.

**Requisitos:**
- Índices en campos de búsqueda frecuente:
  - `usuarios.email` (unique)
  - `actividades.localidad`
  - `actividades.tipo`
  - `actividades.fecha_inicio`
  - `actividades.estado`
- Índice full-text en:
  - `actividades.titulo`
  - `actividades.descripcion`
  - `actividades.etiquetas`
- Índice GiST para coordenadas GPS (PostGIS)
- Queries complejas con EXPLAIN ANALYZE
- Paginación obligatoria en listados

**Criterios de aceptación:**
- No queries con tiempo de ejecución >500ms
- Todas las queries usan índices (no seq scans en tablas grandes)

---

### 4.3 Compatibilidad

#### RNF-008: Compatibilidad de Navegadores
**Descripción:** La aplicación debe funcionar en navegadores modernos.

**Navegadores soportados:**
| Navegador | Versión Mínima |
|-----------|---------------|
| Chrome | 100+ |
| Firefox | 100+ |
| Safari | 15+ |
| Edge | 100+ |

**No soportados:**
- Internet Explorer (cualquier versión)
- Navegadores sin soporte de ES2020

**Criterios de aceptación:**
- 100% funcionalidad en navegadores soportados
- Mensaje de advertencia en navegadores no soportados

---

#### RNF-009: Compatibilidad de Dispositivos
**Descripción:** La aplicación debe funcionar en diferentes dispositivos.

**Dispositivos soportados:**
- Desktop: Windows, macOS, Linux
- Móvil: iOS 14+, Android 10+
- Tablet: iPad, Android tablets

**Resoluciones mínimas:**
- Desktop: 1366x768
- Tablet: 768x1024
- Móvil: 375x667

**Criterios de aceptación:**
- Interfaz completamente funcional en todos los dispositivos
- Touch gestures funcionales en dispositivos táctiles

---

#### RNF-010: API RESTful
**Descripción:** La API debe seguir principios REST.

**Requisitos:**
- Versionado en URL: `/api/v1/`
- Métodos HTTP semánticos:
  - GET: lectura
  - POST: creación
  - PUT/PATCH: actualización
  - DELETE: eliminación
- Códigos de estado HTTP correctos:
  - 200: OK
  - 201: Created
  - 204: No Content
  - 400: Bad Request
  - 401: Unauthorized
  - 403: Forbidden
  - 404: Not Found
  - 409: Conflict
  - 422: Unprocessable Entity
  - 500: Internal Server Error
- Formato JSON para requests y responses
- CORS configurado correctamente
- Content-Type: application/json

**Estructura de respuesta estándar:**
```json
{
  "data": {},
  "message": "string",
  "errors": []
}
```

**Criterios de aceptación:**
- 100% endpoints siguen convenciones REST
- Documentación OpenAPI/Swagger disponible

---

### 4.4 Fiabilidad

#### RNF-011: Disponibilidad
**Descripción:** El sistema debe estar disponible la mayor parte del tiempo.

**Objetivo:** 99% uptime mensual

**Cálculo:**
- 99% uptime = máximo 7.2 horas de downtime por mes
- 99.5% uptime = máximo 3.6 horas de downtime por mes

**Estrategias:**
- Health checks en todos los servicios
- Auto-restart de contenedores caídos
- Monitoreo 24/7 con alertas
- Backups automáticos diarios
- Plan de recuperación ante desastres

**Downtime planificado:**
- Mantenimientos programados fuera de horas pico
- Notificación con 48 horas de anticipación

**Criterios de aceptación:**
- Uptime mensual >= 99%
- RTO (Recovery Time Objective) <4 horas
- RPO (Recovery Point Objective) <24 horas

---

#### RNF-012: Tolerancia a Fallos
**Descripción:** El sistema debe manejar errores gracefully.

**Requisitos:**
- Manejo de excepciones en todos los endpoints
- Logs detallados de errores
- Mensajes de error amigables al usuario
- Fallback para servicios externos (ej: APIs públicas)
- Circuit breaker para servicios dependientes
- Retry logic con exponential backoff

**Ejemplo:**
```python
try:
    result = external_api.fetch_data()
except ExternalAPIError:
    # Log error
    logger.error("External API failed", exc_info=True)
    # Return cached data or graceful degradation
    result = get_cached_data()
```

**Criterios de aceptación:**
- 0% errores no manejados
- Ningún error expone detalles técnicos al usuario final
- Sistema sigue funcionando (degradado) si API externa falla

---

#### RNF-013: Recuperación y Backups
**Descripción:** Los datos deben estar respaldados y recuperables.

**Estrategia de backups:**
- **Base de datos:**
  - Backup completo diario (3:00 AM)
  - Backup incremental cada 6 horas
  - Retención: 30 días
  - Almacenamiento: S3/Cloud Storage
  - Encriptación en reposo
- **Archivos cargados:**
  - Almacenamiento redundante (S3 con versionado)
  - Replicación cross-region

**Plan de recuperación:**
1. Identificar tipo de fallo
2. Notificar stakeholders
3. Restaurar desde backup más reciente
4. Validar integridad de datos
5. Retomar operaciones
6. Post-mortem

**Criterios de aceptación:**
- Backups exitosos 100% del tiempo
- Test de restauración mensual
- RTO <4 horas, RPO <24 horas

---

### 4.5 Seguridad

#### RNF-014: Autenticación y Autorización
**Descripción:** El sistema debe implementar autenticación y autorización seguras.

**Requisitos de autenticación:**
- OAuth2 con Password Grant Type
- JWT con algoritmo RS256 (asimétrico)
- Access token: 30 minutos de vigencia
- Refresh token: 30 días de vigencia
- Refresh token rotation habilitada
- Revocación de tokens
- Rate limiting en login: 5 intentos / 15 min

**Requisitos de contraseña:**
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 número
- Al menos 1 carácter especial
- Hash con bcrypt (cost factor 12+) o Argon2id

**Estructura JWT:**
```json
{
  "sub": "user_id",
  "rol": "usuario|administrador",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Autorización:**
- RBAC (Role-Based Access Control)
- Roles: usuario, administrador
- Decoradores/middlewares para proteger endpoints
- Verificación de permisos en cada request

**Criterios de aceptación:**
- OWASP ASVS v5.0 Nivel 2 cumplimiento en autenticación
- Tokens no almacenados en localStorage (httpOnly cookies preferred)

---

#### RNF-015: Protección contra Ataques Comunes
**Descripción:** El sistema debe estar protegido contra ataques OWASP Top 10.

**Protecciones requeridas:**

**A01 - Broken Access Control:**
- Validación de autorización en cada endpoint
- Usuarios solo acceden a sus propios recursos

**A02 - Cryptographic Failures:**
- HTTPS obligatorio en producción
- Contraseñas hasheadas (bcrypt/Argon2)
- Secrets en variables de entorno
- No datos sensibles en logs

**A03 - Injection:**
- ORM (SQLAlchemy) con prepared statements
- Validación de inputs con Pydantic
- Sanitización de queries de búsqueda

**A04 - Insecure Design:**
- Threat modeling STRIDE
- Security by design

**A05 - Security Misconfiguration:**
- Headers de seguridad:
  ```
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Strict-Transport-Security: max-age=31536000
  Content-Security-Policy: default-src 'self'
  ```
- Deshabilitar debug en producción
- No exponer stack traces

**A06 - Vulnerable Components:**
- Dependencias actualizadas
- Dependabot/Renovate habilitado
- SAST (Bandit, Semgrep)

**A07 - Authentication Failures:**
- Rate limiting
- MFA ready (preparado para futuro)

**A08 - Software and Data Integrity Failures:**
- Firma de JWT
- Validación de integridad en uploads

**A09 - Logging Failures:**
- Logs centralizados
- Alertas en eventos críticos

**A10 - SSRF:**
- Whitelist de URLs externas
- Validación de inputs

**Criterios de aceptación:**
- 0 vulnerabilidades críticas en SAST/DAST
- Compliance con OWASP ASVS Nivel 2

---

#### RNF-016: Protección de Datos Personales
**Descripción:** El sistema debe cumplir con Ley 1581 de 2012 (Colombia).

**Requisitos:**
- Aviso de privacidad claro y accesible
- Consentimiento explícito en registro
- Derecho de acceso: usuario puede ver sus datos
- Derecho de rectificación: usuario puede editar sus datos
- Derecho de supresión: usuario puede solicitar borrado de cuenta
- Datos mínimos necesarios (data minimization)
- Encriptación de datos sensibles en BD (opcional para MVP)
- Logs de acceso a datos personales

**Datos personales recopilados:**
- Email (obligatorio)
- Nombre completo (obligatorio)
- Preferencias (opcional)
- Ubicación preferida (opcional)

**No se recopilan:**
- Documento de identidad
- Información financiera (no hay pagos en MVP)
- Datos biométricos

**Criterios de aceptación:**
- Aviso de privacidad publicado
- Funcionalidad de descarga de datos personales
- Funcionalidad de eliminación de cuenta

---

#### RNF-017: Rate Limiting
**Descripción:** El sistema debe limitar la tasa de requests para prevenir abuso.

**Límites:**
| Endpoint | Límite |
|----------|--------|
| POST /auth/register | 3 / hora / IP |
| POST /auth/login | 5 / 15 min / IP |
| POST /auth/refresh | 10 / hora / usuario |
| GET /actividades/* | 100 / min / usuario |
| POST /favoritos | 20 / min / usuario |
| Endpoints admin | 200 / min / admin |

**Implementación:**
- Redis para almacenar contadores
- Sliding window algorithm
- Headers de respuesta:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 87
  X-RateLimit-Reset: 1640000000
  ```
- Status code 429 Too Many Requests cuando se excede

**Criterios de aceptación:**
- Rate limiting activo en producción
- Ataques de fuerza bruta mitigados

---

### 4.6 Mantenibilidad

#### RNF-018: Código Limpio y Estándares
**Descripción:** El código debe ser legible, mantenible y seguir estándares.

**Backend (Python):**
- PEP 8 (linting con ruff o flake8)
- Type hints en todas las funciones
- Docstrings en módulos, clases y funciones públicas
- Complejidad ciclomática <10 por función
- Cobertura de tests >80%

**Frontend (TypeScript):**
- ESLint con reglas estrictas
- Prettier para formateo
- Componentes funcionales con hooks
- Props con TypeScript interfaces
- Cobertura de tests >70%

**Estructura de proyecto:**
```
backend/
├── app/
│   ├── api/          # Routers
│   ├── core/         # Config, security
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── db/           # Database setup
│   └── main.py
├── tests/
├── requirements.txt
└── Dockerfile

frontend/
├── src/
│   ├── components/   # React components
│   ├── pages/        # Page components
│   ├── services/     # API calls
│   ├── hooks/        # Custom hooks
│   ├── types/        # TypeScript types
│   ├── utils/        # Utilities
│   └── main.tsx
├── tests/
├── package.json
└── Dockerfile
```

**Criterios de aceptación:**
- CI/CD ejecuta linters y falla si hay errores
- Pull requests requieren revisión de código
- Documentación actualizada

---

#### RNF-019: Pruebas Automatizadas
**Descripción:** El sistema debe tener cobertura de pruebas automatizadas.

**Tipos de pruebas:**

**Backend:**
- **Unit tests:** pytest
  - Cobertura >80%
  - Tests de servicios y helpers
- **Integration tests:**
  - Tests de endpoints con TestClient
  - Base de datos de prueba (SQLite o PostgreSQL)
- **E2E tests (opcional MVP):**
  - Playwright para flujos críticos

**Frontend:**
- **Unit tests:** Vitest
  - Cobertura >70%
  - Tests de componentes con React Testing Library
- **E2E tests (opcional MVP):**
  - Playwright para flujos de usuario

**CI/CD:**
- Tests ejecutados en cada push
- Tests bloqueantes para merge
- Reporte de cobertura automático

**Criterios de aceptación:**
- Cobertura backend >80%
- Cobertura frontend >70%
- 0 tests failing en main branch

---

#### RNF-020: Documentación
**Descripción:** El sistema debe estar bien documentado.

**Documentación requerida:**
- **README.md:** Setup, instalación, ejecución
- **API Documentation:** OpenAPI/Swagger generado automáticamente
- **docs/:** 
  - SRS.md (este documento)
  - ARCHITECTURE.md (diagrama de componentes)
  - DEPLOYMENT.md (guía de despliegue)
  - CONTRIBUTING.md (guía para colaboradores)
- **Docstrings:** En código Python
- **Comentarios JSDoc:** En código TypeScript (funciones complejas)

**Criterios de aceptación:**
- Swagger UI accesible en `/docs`
- README con instrucciones claras
- Nuevo desarrollador puede levantar proyecto en <30 min

---

### 4.7 Portabilidad

#### RNF-021: Contenedorización
**Descripción:** El sistema debe estar completamente dockerizado.

**Requisitos:**
- **Backend:** Dockerfile multi-stage
- **Frontend:** Dockerfile multi-stage con Nginx
- **ETL:** Dockerfile para script
- **docker-compose.yml:** Para desarrollo local
  - Backend
  - Frontend
  - PostgreSQL
  - Redis
  - Adminer (opcional)

**Ejemplo docker-compose.yml:**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/triqueta
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=triqueta
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

**Criterios de aceptación:**
- `docker-compose up` levanta todo el stack
- Configuración mediante variables de entorno
- Imágenes optimizadas (<500MB backend, <50MB frontend)

---

#### RNF-022: CI/CD
**Descripción:** El sistema debe tener pipeline de CI/CD automatizado.

**Pipeline stages:**
1. **Lint:** Ejecutar linters (ruff, eslint)
2. **Test:** Ejecutar tests con cobertura
3. **Build:** Construir imágenes Docker
4. **Security Scan:** SAST con Bandit/Semgrep, dependency check
5. **Deploy (manual trigger):** Desplegar a staging/producción

**Herramientas:**
- GitHub Actions (preferred)
- GitLab CI
- Jenkins

**Criterios de aceptación:**
- Pipeline ejecutado en cada push
- Merge bloqueado si pipeline falla
- Deploy automatizado a staging en merge a develop
- Deploy manual a producción desde main

---

### 4.8 Satisfacción del Usuario

#### RNF-023: Net Promoter Score (NPS)
**Descripción:** El sistema debe generar satisfacción en usuarios.

**Objetivo:** NPS >70

**Método de medición:**
- Encuesta post-MVP (después de 2 semanas de uso)
- Pregunta: "¿Qué tan probable es que recomiendes Triqueta Digital? (0-10)"
- Cálculo: % Promoters (9-10) - % Detractors (0-6)

**Criterios de aceptación:**
- NPS >= 70 en encuesta piloto (n>=20)

---

#### RNF-024: Tasa de Adopción
**Descripción:** El sistema debe lograr adopción de usuarios.

**Métricas:**
- Usuarios registrados: >= 200 en primer mes post-lanzamiento
- Usuarios activos mensuales (MAU): >= 100
- Tasa de retención D7: >= 40%
- Tasa de retención D30: >= 20%

**Criterios de aceptación:**
- Cumplir métricas en evaluación post-lanzamiento

---

## Resumen de Requisitos No Funcionales por Categoría

### Usabilidad
- RNF-001: Accesibilidad WCAG 2.1 AA
- RNF-002: Aprendizaje <5 min
- RNF-003: Responsive design

### Eficiencia
- RNF-004: Tiempo respuesta API <2s (P90)
- RNF-005: Tiempo carga frontend (Core Web Vitals)
- RNF-006: Capacidad 200 usuarios concurrentes
- RNF-007: Queries optimizadas

### Compatibilidad
- RNF-008: Navegadores Chrome/Firefox/Safari/Edge 100+
- RNF-009: Dispositivos desktop/móvil/tablet
- RNF-010: API RESTful estándar

### Fiabilidad
- RNF-011: Disponibilidad 99%
- RNF-012: Tolerancia a fallos
- RNF-013: Backups diarios, RTO <4h

### Seguridad
- RNF-014: OAuth2 + JWT
- RNF-015: Protección OWASP Top 10
- RNF-016: Cumplimiento Ley 1581/2012
- RNF-017: Rate limiting

### Mantenibilidad
- RNF-018: Código limpio, linters
- RNF-019: Tests >80% backend, >70% frontend
- RNF-020: Documentación completa

### Portabilidad
- RNF-021: Docker Compose
- RNF-022: CI/CD automatizado

### Satisfacción
- RNF-023: NPS >70
- RNF-024: Adopción >= 200 usuarios

---

## Matriz de Trazabilidad: Requisitos No Funcionales → ISO/IEC 25010:2023

| ISO/IEC 25010 | Característica | RNF |
|---------------|----------------|-----|
| 4.1 | Functional Suitability | RF-001 a RF-022 |
| 4.2 | Performance Efficiency | RNF-004, RNF-005, RNF-006, RNF-007 |
| 4.3 | Compatibility | RNF-008, RNF-009, RNF-010 |
| 4.4 | Usability | RNF-001, RNF-002, RNF-003 |
| 4.5 | Reliability | RNF-011, RNF-012, RNF-013 |
| 4.6 | Security | RNF-014, RNF-015, RNF-016, RNF-017 |
| 4.7 | Maintainability | RNF-018, RNF-019, RNF-020 |
| 4.8 | Portability | RNF-021, RNF-022 |
