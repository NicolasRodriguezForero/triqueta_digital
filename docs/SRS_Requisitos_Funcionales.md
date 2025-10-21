# Requisitos Funcionales - Triqueta Digital

## 3. Requisitos Funcionales

### 3.1 Módulo de Autenticación y Gestión de Usuarios

#### RF-001: Registro de Usuario
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir el registro de nuevos usuarios mediante email y contraseña.

**Entradas:**
- Email válido
- Contraseña (mínimo 8 caracteres, al menos 1 mayúscula, 1 número, 1 carácter especial)
- Nombre completo
- Aceptación de términos y condiciones

**Proceso:**
1. Validar formato de email
2. Verificar que el email no esté registrado
3. Hash de contraseña (bcrypt o Argon2)
4. Crear usuario con rol "usuario"
5. Generar tokens JWT (access + refresh)

**Salidas:**
- Usuario creado en base de datos
- Access token (válido 30 min)
- Refresh token (válido 30 días)
- Mensaje de confirmación

**Criterios de aceptación:**
- El email debe ser único en el sistema
- La contraseña debe cumplir política de seguridad
- Los tokens generados deben ser válidos

---

#### RF-002: Login de Usuario
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir la autenticación mediante OAuth2 con flujo password grant.

**Entradas:**
- Email
- Contraseña

**Proceso:**
1. Buscar usuario por email
2. Verificar hash de contraseña
3. Generar access token (30 minutos)
4. Generar refresh token (30 días)
5. Registrar último acceso

**Salidas:**
- Access token (JWT)
- Refresh token (JWT)
- Información básica del usuario (id, nombre, rol)

**Criterios de aceptación:**
- Credenciales válidas permiten acceso
- Credenciales inválidas retornan error 401
- Tokens incluyen claims: user_id, rol, exp

---

#### RF-003: Refresh Token
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir renovar el access token usando un refresh token válido.

**Entradas:**
- Refresh token válido

**Proceso:**
1. Validar refresh token
2. Verificar que no esté revocado
3. Generar nuevo access token
4. Opcionalmente rotar refresh token

**Salidas:**
- Nuevo access token
- Nuevo refresh token (si rotación habilitada)

**Criterios de aceptación:**
- Solo tokens válidos y no revocados permiten refresh
- Tokens expirados retornan error 401

---

#### RF-004: Logout de Usuario
**Prioridad:** Media  
**Descripción:** El sistema debe permitir cerrar sesión revocando los tokens.

**Entradas:**
- Refresh token

**Proceso:**
1. Marcar refresh token como revocado en BD
2. Registrar evento de logout

**Salidas:**
- Confirmación de logout

**Criterios de aceptación:**
- El refresh token queda invalidado
- No se puede renovar access token con ese refresh token

---

#### RF-005: Gestión de Perfil de Usuario
**Prioridad:** Alta  
**Descripción:** El usuario debe poder ver y actualizar su información de perfil.

**Campos editables:**
- Nombre completo
- Foto de perfil (URL)
- Etiquetas de interés (array de strings)
- Disponibilidad horaria preferida
- Localidad de preferencia
- Nivel de actividad física preferido

**Proceso:**
1. Autenticar usuario
2. Validar campos enviados
3. Actualizar registro en BD
4. Retornar perfil actualizado

**Criterios de aceptación:**
- Solo el usuario autenticado puede editar su propio perfil
- Las etiquetas deben ser validadas contra lista permitida

---

### 3.2 Módulo de Actividades

#### RF-006: Listar Actividades
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir listar actividades con paginación y filtros.

**Filtros disponibles:**
- `tipo`: cultura, deporte, recreación
- `localidad`: Chapinero, Santa Fe, La Candelaria
- `fecha_desde`: fecha ISO 8601
- `fecha_hasta`: fecha ISO 8601
- `precio_min`: número
- `precio_max`: número
- `es_gratis`: boolean
- `nivel_actividad`: bajo, medio, alto
- `etiquetas`: array de strings

**Parámetros de paginación:**
- `page`: número de página (default: 1)
- `page_size`: tamaño de página (default: 20, max: 100)

**Proceso:**
1. Validar filtros y parámetros
2. Construir query SQL con filtros aplicados
3. Ejecutar query con LIMIT/OFFSET para paginación
4. Calcular metadata de paginación
5. Retornar respuesta

**Salidas:**
```json
{
  "data": [
    {
      "id": "uuid",
      "titulo": "string",
      "descripcion_corta": "string",
      "imagen_url": "string",
      "fecha_inicio": "datetime",
      "localidad": "string",
      "precio": "number",
      "es_gratis": "boolean",
      "etiquetas": ["string"],
      "popularidad": "number"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

**Criterios de aceptación:**
- Filtros se aplican correctamente en combinación
- Paginación funciona correctamente
- Tiempo de respuesta <2s para queries normales

---

#### RF-007: Ver Detalle de Actividad
**Prioridad:** Alta  
**Descripción:** El sistema debe mostrar información completa de una actividad.

**Entradas:**
- ID de actividad (UUID)

**Salidas:**
- Título
- Descripción completa (markdown o HTML)
- Tipo de actividad
- Fecha y hora inicio/fin
- Ubicación (dirección, coordenadas GPS)
- Localidad
- Precio
- Es gratis (boolean)
- Nivel de actividad física
- Etiquetas
- Información de contacto
- Enlace externo
- Fuente de datos
- Popularidad (score)
- Fecha de creación
- Fecha de última actualización

**Proceso:**
1. Validar UUID
2. Query a BD
3. Registrar vista (para popularidad)
4. Retornar actividad completa

**Criterios de aceptación:**
- Actividad existente retorna información completa
- Actividad inexistente retorna error 404
- Vista se registra máximo 1 vez por usuario por día

---

#### RF-008: Búsqueda de Actividades
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir búsqueda por palabras clave.

**Entradas:**
- `q`: query de búsqueda (texto libre)
- Filtros opcionales (localidad, tipo, fecha, etc.)
- Parámetros de paginación

**Proceso:**
1. Sanitizar query de búsqueda
2. Aplicar búsqueda full-text en campos:
   - `titulo` (peso 3)
   - `descripcion` (peso 2)
   - `etiquetas` (peso 4)
3. Aplicar filtros adicionales
4. Ordenar por relevancia (score de búsqueda)
5. Paginar resultados

**Salidas:**
- Lista de actividades coincidentes (mismo formato que RF-006)
- Cada resultado incluye score de relevancia

**Criterios de aceptación:**
- Búsqueda encuentra coincidencias parciales
- Búsqueda es case-insensitive
- Acentos son ignorados (búsqueda normalizada)
- Tiempo de respuesta <2s

---

#### RF-009: CRUD de Actividades (Administrador)
**Prioridad:** Alta  
**Descripción:** Los administradores deben poder crear, editar y eliminar actividades.

**Operaciones:**

**Crear Actividad:**
```
POST /api/v1/actividades
Headers: Authorization: Bearer <admin_token>
Body: {
  "titulo": "string" (required),
  "descripcion": "string" (required),
  "tipo": "cultura|deporte|recreacion" (required),
  "fecha_inicio": "datetime" (required),
  "fecha_fin": "datetime" (optional),
  "ubicacion_direccion": "string" (required),
  "ubicacion_lat": "float" (required),
  "ubicacion_lng": "float" (required),
  "localidad": "Chapinero|Santa Fe|La Candelaria" (required),
  "precio": "float" (default: 0),
  "es_gratis": "boolean" (default: true),
  "nivel_actividad": "bajo|medio|alto" (optional),
  "etiquetas": ["string"] (required),
  "contacto": "string" (optional),
  "enlace_externo": "url" (optional),
  "fuente": "string" (default: "manual")
}
```

**Actualizar Actividad:**
```
PUT /api/v1/actividades/{id}
Headers: Authorization: Bearer <admin_token>
Body: { campos a actualizar }
```

**Eliminar Actividad (Soft Delete):**
```
DELETE /api/v1/actividades/{id}
Headers: Authorization: Bearer <admin_token>
```

**Criterios de aceptación:**
- Solo usuarios con rol "administrador" pueden realizar operaciones
- Fechas de actividades deben ser futuras al crear
- Actividades eliminadas tienen estado "inactiva" pero no se borran de BD
- Actividades inactivas no aparecen en búsquedas públicas

---

#### RF-010: Importación Manual de Actividades
**Prioridad:** Media  
**Descripción:** Los administradores deben poder importar actividades desde archivo CSV/JSON.

**Entradas:**
- Archivo CSV o JSON
- Formato definido en documentación

**Formato CSV esperado:**
```
titulo,descripcion,tipo,fecha_inicio,fecha_fin,ubicacion_direccion,ubicacion_lat,ubicacion_lng,localidad,precio,es_gratis,nivel_actividad,etiquetas,contacto,enlace_externo,fuente
```

**Proceso:**
1. Validar formato de archivo
2. Parsear contenido
3. Validar cada registro:
   - Campos obligatorios presentes
   - Formatos correctos
   - Detectar duplicados (titulo + fecha + ubicación)
4. Insertar actividades válidas con estado "pendiente_validacion"
5. Generar reporte detallado

**Salidas:**
```json
{
  "resumen": {
    "total_procesados": 100,
    "exitosos": 85,
    "duplicados": 10,
    "errores": 5
  },
  "errores_detalle": [
    {
      "fila": 15,
      "error": "Campo 'fecha_inicio' inválido"
    }
  ]
}
```

**Criterios de aceptación:**
- Solo administradores pueden importar
- Registros inválidos se reportan sin detener proceso
- Duplicados se detectan y reportan

---

### 3.3 Módulo de Favoritos

#### RF-011: Guardar Actividad como Favorito
**Prioridad:** Alta  
**Descripción:** Los usuarios deben poder marcar actividades como favoritas.

**Entradas:**
- ID de actividad

**Proceso:**
1. Autenticar usuario
2. Verificar que actividad existe y está activa
3. Crear registro en tabla `favoritos` (user_id, actividad_id, fecha_guardado)
4. Incrementar campo `popularidad_favoritos` en actividad

**Salidas:**
- Confirmación: `{"message": "Actividad guardada como favorita"}`

**Criterios de aceptación:**
- Usuario autenticado puede guardar favoritos
- No se permiten duplicados (constraint unique en BD)
- Guardar favorito duplicado retorna 409 Conflict

---

#### RF-012: Listar Favoritos del Usuario
**Prioridad:** Alta  
**Descripción:** El usuario debe poder ver sus actividades favoritas.

**Proceso:**
1. Autenticar usuario
2. Query JOIN entre favoritos y actividades
3. Filtrar por user_id y actividades activas
4. Ordenar por fecha_guardado DESC
5. Paginar resultados

**Salidas:**
- Lista de actividades favoritas (mismo formato que RF-006)
- Incluye campo adicional: `fecha_guardado`

**Criterios de aceptación:**
- Solo se muestran favoritos del usuario autenticado
- Actividades eliminadas/inactivas no aparecen

---

#### RF-013: Eliminar Favorito
**Prioridad:** Media  
**Descripción:** El usuario debe poder quitar una actividad de favoritos.

**Entradas:**
- ID de actividad

**Proceso:**
1. Autenticar usuario
2. Eliminar registro de tabla `favoritos` WHERE user_id = X AND actividad_id = Y
3. Decrementar campo `popularidad_favoritos` en actividad

**Salidas:**
- Confirmación: `{"message": "Favorito eliminado"}`

**Criterios de aceptación:**
- Solo el usuario propietario puede eliminar su favorito
- Eliminar favorito inexistente retorna 404

---

### 3.4 Módulo de Recomendaciones (IA)

#### RF-014: Obtener Recomendaciones Personalizadas
**Prioridad:** Alta  
**Descripción:** El sistema debe generar recomendaciones basadas en etiquetas del usuario y popularidad.

**Entradas:**
- ID de usuario (implícito por token JWT)
- `limit`: cantidad de recomendaciones (default: 10, max: 50)

**Algoritmo MVP:**

```python
def calcular_score_recomendacion(actividad, usuario):
    score = 0
    
    # Base: Popularidad (0-100)
    score += actividad.popularidad_normalizada * 100
    
    # Bonus por etiquetas coincidentes
    etiquetas_usuario = set(usuario.etiquetas_interes)
    etiquetas_actividad = set(actividad.etiquetas)
    coincidencias = etiquetas_usuario.intersection(etiquetas_actividad)
    score += len(coincidencias) * 10
    
    # Bonus por localidad preferida
    if actividad.localidad == usuario.localidad_preferida:
        score += 5
    
    # Bonus por disponibilidad horaria
    if hora_actividad in usuario.disponibilidad_horaria:
        score += 3
    
    # Penalización si ya es favorito
    if actividad in usuario.favoritos:
        score = 0  # Excluir
    
    return score
```

**Proceso:**
1. Obtener perfil completo del usuario
2. Query actividades activas con fecha >= hoy
3. Calcular score para cada actividad
4. Ordenar por score DESC
5. Filtrar actividades con score > 0
6. Tomar top N
7. Generar explicación para cada recomendación

**Salidas:**
```json
{
  "recomendaciones": [
    {
      "actividad": { /* datos completos */ },
      "score": 125.5,
      "explicacion": "Recomendado porque te gusta 'arte' y 'música'"
    }
  ]
}
```

**Criterios de aceptación:**
- Usuarios sin etiquetas reciben recomendaciones basadas solo en popularidad
- Explicación debe ser comprensible y específica
- Tiempo de generación <1s para 10 recomendaciones

---

#### RF-015: Actualizar Scoring de Popularidad
**Prioridad:** Media  
**Descripción:** El sistema debe actualizar automáticamente el score de popularidad.

**Componentes del score:**
- `popularidad_favoritos`: contador de favoritos
- `popularidad_vistas`: contador de vistas (limitado 1/usuario/día)

**Score normalizado:**
```python
popularidad_normalizada = (
    (favoritos * 1.0) + (vistas * 0.1)
) / max_popularidad_sistema
```

**Eventos que actualizan:**
- Usuario guarda favorito: `popularidad_favoritos += 1`
- Usuario elimina favorito: `popularidad_favoritos -= 1`
- Vista de detalle: `popularidad_vistas += 0.1` (máx 1/user/día)

**Proceso:**
- Actualizar en tiempo real al ocurrir evento
- Recalcular `popularidad_normalizada` diariamente (batch job)

**Criterios de aceptación:**
- Score refleja interacción real
- No se puede inflar artificialmente (límites por usuario)

---

### 3.5 Módulo de Gestión de Ingesta (ETL Manager)

#### RF-016: Dashboard de Estado de Ingesta
**Prioridad:** Media  
**Descripción:** Los administradores deben poder ver el estado de procesos ETL.

**Información mostrada:**
- Última ejecución: fecha, hora, duración
- Estado: éxito, error, corriendo
- Actividades importadas: total
- Actividades pendientes validación
- Errores reportados: lista
- Fuentes de datos: lista con estado
- Próxima ejecución programada (si aplica)

**Endpoint:** `GET /api/v1/admin/etl/status`

**Criterios de aceptación:**
- Solo administradores acceden
- Información en tiempo real si hay proceso corriendo

---

#### RF-017: Activar Proceso de Ingesta Manual
**Prioridad:** Media  
**Descripción:** Los administradores deben poder ejecutar manualmente el script ETL.

**Endpoint:** `POST /api/v1/admin/etl/run`

**Proceso:**
1. Verificar permisos de admin
2. Verificar que no hay otro proceso ETL corriendo
3. Ejecutar script ETL Docker:
   ```bash
   docker run --network=triqueta_network \
              -e DATABASE_URL=$DB_URL \
              triqueta-etl:latest
   ```
4. Registrar inicio en tabla `etl_executions`
5. Retornar ID de ejecución

**Salidas:**
```json
{
  "execution_id": "uuid",
  "status": "running",
  "started_at": "datetime"
}
```

**Monitoreo:**
- Frontend puede consultar logs vía SSE o polling
- Endpoint: `GET /api/v1/admin/etl/executions/{id}/logs`

**Criterios de aceptación:**
- Solo administradores pueden activar
- No se permiten ejecuciones concurrentes
- Timeout de ejecución: 1 hora

---

#### RF-018: Validar Actividades Importadas
**Prioridad:** Media  
**Descripción:** Los administradores deben poder revisar y validar actividades importadas.

**Endpoint:** `GET /api/v1/admin/actividades?estado=pendiente_validacion`

**Acciones disponibles:**
- **Aprobar:** `POST /api/v1/admin/actividades/{id}/aprobar`
  - Cambiar estado a "activa"
- **Editar y Aprobar:** `PUT /api/v1/admin/actividades/{id}` + aprobar
  - Editar campos + cambiar estado a "activa"
- **Rechazar:** `POST /api/v1/admin/actividades/{id}/rechazar`
  - Cambiar estado a "rechazada"
  - Opcionalmente agregar nota de rechazo

**Criterios de aceptación:**
- Solo actividades con estado "activa" aparecen en búsquedas públicas
- Administradores pueden ver actividades en cualquier estado
- Actividades rechazadas se mantienen en BD para auditoría

---

### 3.6 Módulo de Dispositivos IoT

#### RF-019: Vincular Dispositivo IoT
**Prioridad:** Baja (post-MVP)  
**Descripción:** Los usuarios deben poder vincular un dispositivo IoT a su cuenta.

**Entradas:**
- `device_code`: código único del dispositivo (ej: "TRIQ-ABC123")

**Proceso:**
1. Autenticar usuario
2. Validar que código existe en tabla `dispositivos`
3. Verificar que dispositivo no esté ya vinculado
4. Crear relación en tabla `usuarios_dispositivos`
5. Generar token JWT de dispositivo (válido 1 año)

**Salidas:**
```json
{
  "device_id": "uuid",
  "device_token": "jwt_token",
  "vinculado_at": "datetime"
}
```

**Criterios de aceptación:**
- Un dispositivo solo puede estar vinculado a un usuario a la vez
- Usuario puede desvincular dispositivo
- Token de dispositivo tiene claims: device_id, user_id, exp

---

#### RF-020: API de Sincronización para Dispositivo
**Prioridad:** Baja (post-MVP)  
**Descripción:** El dispositivo IoT debe poder obtener recomendaciones del usuario vinculado.

**Endpoint:** `GET /api/v1/iot/recommendations`

**Headers:**
- `Authorization: Bearer <device_token>`

**Proceso:**
1. Validar token de dispositivo
2. Obtener user_id asociado
3. Generar recomendaciones (algoritmo RF-014)
4. Filtrar top 3-5
5. Retornar información simplificada para display

**Salidas:**
```json
{
  "recommendations": [
    {
      "titulo": "string (max 50 chars)",
      "fecha": "datetime",
      "localidad": "string",
      "tipo": "string"
    }
  ],
  "last_updated": "datetime"
}
```

**Criterios de aceptación:**
- Solo dispositivos vinculados y autenticados acceden
- Respuesta optimizada para display limitado
- Actualización cada 1 hora o bajo demanda

---

### 3.7 Módulo de Administración

#### RF-021: Dashboard de Administración
**Prioridad:** Media  
**Descripción:** Los administradores deben tener un dashboard con métricas clave.

**Métricas mostradas:**

**Usuarios:**
- Total de usuarios registrados
- Usuarios activos (últimos 7/30 días)
- Nuevos usuarios (última semana)

**Actividades:**
- Total de actividades activas
- Actividades por localidad (gráfico de torta)
- Actividades por tipo (gráfico de barras)
- Actividades pendientes de validación

**Interacción:**
- Top 10 actividades más populares
- Top 10 etiquetas más usadas
- Total de favoritos guardados

**Sistema:**
- Última ejecución ETL
- Búsquedas recientes (últimas 20)

**Endpoint:** `GET /api/v1/admin/dashboard`

**Criterios de aceptación:**
- Solo administradores acceden
- Datos actualizados cada 5 minutos (caché)
- Gráficos simples y claros en frontend

---

#### RF-022: Gestión de Usuarios (Administrador)
**Prioridad:** Baja  
**Descripción:** Los administradores deben poder gestionar usuarios.

**Operaciones:**

**Listar Usuarios:**
```
GET /api/v1/admin/usuarios
Parámetros: page, page_size, rol, estado
```

**Ver Detalle:**
```
GET /api/v1/admin/usuarios/{id}
Respuesta: perfil completo + actividad reciente
```

**Cambiar Rol:**
```
PATCH /api/v1/admin/usuarios/{id}/rol
Body: {"rol": "administrador" | "usuario"}
```

**Desactivar/Activar Cuenta:**
```
PATCH /api/v1/admin/usuarios/{id}/estado
Body: {"activo": true | false}
```

**Criterios de aceptación:**
- Solo administradores acceden
- Admin no puede autodesactivarse
- Admin no puede quitarse rol de administrador (requiere otro admin)
- Se registra auditoría de cambios en tabla `audit_logs`

---

## Resumen de Prioridades

### Alta Prioridad (MVP Core):
- RF-001 a RF-005: Autenticación
- RF-006 a RF-009: Actividades
- RF-011 a RF-014: Favoritos y Recomendaciones

### Media Prioridad (MVP Extendido):
- RF-010: Importación manual
- RF-015 a RF-018: Gestión ETL
- RF-021: Dashboard admin

### Baja Prioridad (Post-MVP):
- RF-019 a RF-020: Dispositivos IoT
- RF-022: Gestión avanzada de usuarios
