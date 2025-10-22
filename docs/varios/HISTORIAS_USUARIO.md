# Historias de Usuario - Triqueta Digital

**Proyecto:** Triqueta Digital  
**Versión:** 1.0  
**Fecha:** Octubre 2025  
**Total de Historias:** 35

---

## 📚 Índice de Módulos

1. [Autenticación y Gestión de Usuarios](#1-autenticación-y-gestión-de-usuarios) - 5 historias
2. [Actividades](#2-actividades) - 8 historias
3. [Favoritos](#3-favoritos) - 3 historias
4. [Recomendaciones (IA)](#4-recomendaciones-ia) - 2 historias
5. [Perfil de Usuario](#5-perfil-de-usuario) - 2 historias
6. [Administración](#6-administración) - 9 historias
7. [Gestión de Ingesta (ETL)](#7-gestión-de-ingesta-etl) - 4 historias
8. [Dispositivos IoT](#8-dispositivos-iot) - 2 historias

---

## 1. Autenticación y Gestión de Usuarios

### HU-001: Registro de Usuario

**Como:** Usuario no autenticado  
**Quiero:** Registrarme en la plataforma con mi email y contraseña  
**Para:** Crear una cuenta y acceder a las funcionalidades de la plataforma  

**Prioridad:** Alta

**Criterios de aceptación:**
- El formulario solicita: email, contraseña, confirmación de contraseña y nombre completo
- El email debe tener formato válido y no estar registrado
- La contraseña debe cumplir requisitos: mínimo 8 caracteres, 1 mayúscula, 1 número, 1 carácter especial
- Se debe aceptar términos y condiciones
- Al registrarse se generan access token y refresh token automáticamente
- Se redirige a la página principal con mensaje de confirmación
- Errores se muestran de forma descriptiva

---

### HU-002: Inicio de Sesión

**Como:** Usuario registrado  
**Quiero:** Iniciar sesión con mi email y contraseña  
**Para:** Acceder a mi cuenta y utilizar la plataforma  

**Prioridad:** Alta

**Criterios de aceptación:**
- El formulario solicita email y contraseña
- Si las credenciales son correctas, se generan tokens (access 30 min, refresh 30 días)
- Se redirige a la página principal con mensaje de bienvenida
- Credenciales incorrectas muestran mensaje de error genérico
- Rate limiting: máximo 5 intentos cada 15 minutos
- Después de 5 intentos, se bloquea temporalmente el acceso

---

### HU-003: Cierre de Sesión

**Como:** Usuario registrado  
**Quiero:** Cerrar mi sesión de forma segura  
**Para:** Proteger mi cuenta cuando termine de usar la plataforma  

**Prioridad:** Media

**Criterios de aceptación:**
- Botón "Cerrar sesión" visible en header/menú
- Al hacer clic, se revoca el refresh token
- Se elimina información de sesión del cliente
- Usuario es redirigido a página de inicio con mensaje de confirmación
- No se puede acceder a páginas protegidas después del logout

---

### HU-004: Renovación Automática de Sesión

**Como:** Usuario registrado  
**Quiero:** Que mi sesión se renueve automáticamente  
**Para:** No tener que iniciar sesión constantemente  

**Prioridad:** Alta

**Criterios de aceptación:**
- Cuando el access token está por expirar (<5 min), se renueva automáticamente
- El sistema usa el refresh token para obtener nuevo access token
- El proceso es transparente (sin interrumpir navegación)
- Si refresh token ha expirado, se redirige al login
- Las peticiones en curso no fallan durante renovación

---

### HU-005: Recuperación de Contraseña

**Como:** Usuario registrado  
**Quiero:** Recuperar mi contraseña si la olvido  
**Para:** Poder acceder nuevamente a mi cuenta  

**Prioridad:** Media

**Criterios de aceptación:**
- Enlace "¿Olvidaste tu contraseña?" en página de login
- Usuario ingresa su email registrado
- Sistema envía email con enlace de recuperación (válido 1 hora)
- El enlace redirige a página para establecer nueva contraseña
- Nueva contraseña debe cumplir requisitos de seguridad
- Al cambiar contraseña, se invalidan todos los refresh tokens previos
- Se muestra mensaje de confirmación

---

## 2. Actividades

### HU-006: Explorar Actividades

**Como:** Usuario no autenticado  
**Quiero:** Ver un listado de actividades culturales, recreativas y deportivas  
**Para:** Conocer la oferta disponible en mi localidad  

**Prioridad:** Alta

**Criterios de aceptación:**
- Página muestra listado en formato de tarjetas (grid responsive)
- Cada tarjeta: título, imagen, localidad, tipo, fecha, precio, etiquetas
- Paginación de 20 actividades por página
- Se muestra total de actividades encontradas
- Skeleton loaders mientras carga
- Lazy loading de imágenes
- Mensaje informativo si no hay actividades

---

### HU-007: Filtrar Actividades

**Como:** Usuario no autenticado  
**Quiero:** Filtrar actividades por tipo, localidad, fecha y precio  
**Para:** Encontrar actividades que se ajusten a mis preferencias  

**Prioridad:** Alta

**Criterios de aceptación:**
- Panel lateral/sheet con filtros: tipo, localidad, rango de fechas, precio, actividades gratuitas, nivel, etiquetas
- Los filtros se aplican individualmente o en combinación
- Listado se actualiza automáticamente al aplicar filtros
- Se muestra número de resultados encontrados
- Filtros aplicados son visibles (badges/tags)
- Botón "Limpiar filtros" para resetear
- Filtros persisten al navegar entre páginas
- En móvil, filtros en drawer/sheet

---

### HU-008: Buscar Actividades

**Como:** Usuario no autenticado  
**Quiero:** Buscar actividades por palabras clave  
**Para:** Encontrar rápidamente actividades específicas  

**Prioridad:** Alta

**Criterios de aceptación:**
- Barra de búsqueda visible en página de actividades
- Búsqueda en: título, descripción y etiquetas
- Resultados ordenados por relevancia
- Búsqueda case-insensitive y sin acentos
- Coincidencias parciales permitidas
- Se puede combinar búsqueda con filtros
- Mensaje si no hay resultados

---

### HU-009: Ver Detalle de Actividad

**Como:** Usuario no autenticado  
**Quiero:** Ver información completa de una actividad  
**Para:** Conocer todos los detalles antes de participar  

**Prioridad:** Alta

**Criterios de aceptación:**
- Página muestra: título, imagen, descripción completa, tipo, fecha/hora, ubicación, localidad, precio, nivel, etiquetas, contacto, enlace externo, fuente
- Botón "Volver" a la lista
- Responsive en todos los dispositivos
- Se registra la vista (para popularidad)

---

### HU-010: Crear Actividad (Admin)

**Como:** Administrador  
**Quiero:** Crear una nueva actividad manualmente  
**Para:** Agregar ofertas al catálogo  

**Prioridad:** Alta

**Criterios de aceptación:**
- Solo rol "administrador" puede acceder
- Botón "Nueva Actividad" en panel admin
- Formulario con campos obligatorios: título, descripción, tipo, fecha, ubicación, localidad, precio, nivel, etiquetas (mín 1)
- Campos opcionales: fecha fin, contacto, enlace
- Validación en tiempo real
- Vista previa antes de guardar
- Actividad se crea con estado "activa"
- Mensaje de confirmación y redirección a listado

---

### HU-011: Editar Actividad (Admin)

**Como:** Administrador  
**Quiero:** Editar información de una actividad existente  
**Para:** Corregir errores o actualizar datos  

**Prioridad:** Alta

**Criterios de aceptación:**
- Solo rol "administrador" puede acceder
- Botón "Editar" en cada actividad del listado admin
- Formulario precargado con datos actuales
- Se pueden modificar todos los campos
- Validaciones aplican igual que al crear
- Botón "Cancelar" descarta cambios
- Al guardar, se actualiza "updated_at"
- Mensaje de confirmación y cambios reflejados inmediatamente

---

### HU-012: Eliminar Actividad (Admin)

**Como:** Administrador  
**Quiero:** Eliminar actividades obsoletas o incorrectas  
**Para:** Mantener catálogo actualizado  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo rol "administrador" puede acceder
- Botón "Eliminar" en cada actividad
- Dialog de confirmación explicando soft delete
- Al confirmar, actividad cambia estado a "inactiva"
- NO se elimina físicamente de BD
- Actividades inactivas no aparecen en búsquedas públicas
- Se pueden ver en panel admin con filtro especial
- Opción para "restaurar" actividades inactivas

---

### HU-013: Importar Actividades CSV/JSON (Admin)

**Como:** Administrador  
**Quiero:** Importar actividades masivamente desde archivo  
**Para:** Agregar múltiples actividades eficientemente  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo rol "administrador" puede acceder
- Página /admin/actividades/importar con documentación de formato
- Drag & drop o selección de archivo (.csv, .json)
- Barra de progreso durante procesamiento
- Sistema valida campos, formatos y detecta duplicados
- Resumen al finalizar: total, exitosos, duplicados, errores (con detalle)
- Actividades importadas con estado "pendiente_validacion"
- Opción para descargar archivo de errores

---

## 3. Favoritos

### HU-014: Guardar Actividad como Favorita

**Como:** Usuario registrado  
**Quiero:** Marcar una actividad como favorita  
**Para:** Guardarla y acceder fácilmente después  

**Prioridad:** Alta

**Criterios de aceptación:**
- Solo usuarios autenticados pueden guardar
- Botón de "corazón" en cada tarjeta
- Al hacer clic, se guarda como favorita
- Ícono cambia visualmente (relleno/color)
- Notificación breve "Añadido a favoritos"
- Si no está autenticado, pide iniciar sesión
- No se permiten duplicados
- Acción reversible

---

### HU-015: Ver Mis Favoritos

**Como:** Usuario registrado  
**Quiero:** Ver listado de mis actividades favoritas  
**Para:** Revisar actividades que me interesan  

**Prioridad:** Alta

**Criterios de aceptación:**
- Solo usuarios autenticados acceden a /favoritos
- Muestra todas las actividades guardadas
- Formato de tarjetas igual que listado general
- Ordenadas por fecha de guardado (recientes primero)
- Incluye fecha en que se guardó
- Total de favoritos visible
- Mensaje si no hay favoritos invitando a explorar
- Actividades inactivas no se muestran
- Botón "Quitar de favoritos" en cada tarjeta
- Responsive

---

### HU-016: Quitar Actividad de Favoritos

**Como:** Usuario registrado  
**Quiero:** Eliminar actividad de mis favoritos  
**Para:** Mantener lista actualizada  

**Prioridad:** Media

**Criterios de aceptación:**
- Botón de favorito permite quitar favoritos
- Al hacer clic en actividad favorita, se elimina
- Ícono cambia visualmente (vacío/color diferente)
- Notificación "Eliminado de favoritos"
- Cambio inmediato en todas las vistas
- En página de favoritos, botón "Quitar" disponible
- Tarjeta desaparece con animación
- No requiere confirmación (es reversible)

---

## 4. Recomendaciones (IA)

### HU-017: Recibir Recomendaciones Personalizadas

**Como:** Usuario registrado  
**Quiero:** Recibir recomendaciones basadas en mis intereses  
**Para:** Descubrir actividades relevantes automáticamente  

**Prioridad:** Alta

**Criterios de aceptación:**
- Solo usuarios autenticados acceden a /recomendaciones
- Sistema usa algoritmo híbrido: popularidad, etiquetas, localidad, disponibilidad
- Se muestran 10 recomendaciones por defecto
- Actividades favoritas NO se recomiendan
- Cada recomendación: información de actividad, score (opcional), explicación breve
- Se pueden refrescar recomendaciones
- Si usuario sin etiquetas, recomendaciones por popularidad
- Responsive y cacheadas para performance

---

### HU-018: Ver Explicación de Recomendación

**Como:** Usuario registrado  
**Quiero:** Entender por qué se recomienda una actividad  
**Para:** Confiar en las recomendaciones  

**Prioridad:** Media

**Criterios de aceptación:**
- Cada tarjeta incluye explicación breve
- Explicación menciona: etiquetas coincidentes, localidad, popularidad, disponibilidad
- Lenguaje claro y natural (no técnico)
- Se pueden ver múltiples razones si aplican
- Opcional: ícono de información para expandir/colapsar

---

## 5. Perfil de Usuario

### HU-019: Ver Mi Perfil

**Como:** Usuario registrado  
**Quiero:** Ver mi información de perfil  
**Para:** Revisar mis datos y preferencias  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo usuarios autenticados acceden a /profile
- Muestra: nombre, email, foto, etiquetas de interés, localidad preferida, disponibilidad horaria, nivel de actividad
- Botón "Editar perfil"
- Estadísticas: total de favoritos, actividades vistas
- Responsive

---

### HU-020: Editar Mi Perfil

**Como:** Usuario registrado  
**Quiero:** Actualizar mi información de perfil  
**Para:** Personalizar mi experiencia en la plataforma  

**Prioridad:** Alta

**Criterios de aceptación:**
- Formulario editable con: nombre, foto URL, etiquetas de interés, localidad preferida, disponibilidad horaria, nivel de actividad
- Validación en tiempo real
- Etiquetas validadas contra lista permitida
- Botón "Guardar" y "Cancelar"
- Al guardar, perfil actualizado inmediatamente
- Mensaje de confirmación
- Solo usuario propietario puede editar su perfil

---

## 6. Administración

### HU-021: Ver Dashboard de Administración

**Como:** Administrador  
**Quiero:** Ver métricas clave en un dashboard  
**Para:** Monitorear estado y uso de la plataforma  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo rol "administrador" accede a /admin/dashboard
- Métricas: usuarios (total, activos 7d/30d, nuevos), actividades (total, por localidad, por tipo, pendientes), interacción (favoritos, top 10 actividades, top 10 etiquetas), sistema (última ejecución ETL, búsquedas recientes)
- Gráficos visuales (torta, barras)
- Actualización cada 5 minutos (caché)
- Botón refrescar manual
- Responsive con iconos descriptivos

---

### HU-022: Gestionar Usuarios (Admin)

**Como:** Administrador  
**Quiero:** Ver y gestionar usuarios  
**Para:** Administrar roles y estados de cuentas  

**Prioridad:** Baja

**Criterios de aceptación:**
- Solo rol "administrador" accede a /admin/usuarios
- Listado con: email, nombre, rol, estado, fecha registro, último acceso
- Paginado y filtrable por rol y estado
- Búsqueda por email o nombre
- Acciones: ver detalle, cambiar rol, activar/desactivar
- Acciones requieren confirmación
- Admin NO puede autodesactivarse ni quitarse su rol
- Logs de auditoría de acciones
- Mensaje de confirmación

---

### HU-023: Ver Detalle de Usuario (Admin)

**Como:** Administrador  
**Quiero:** Ver información detallada de un usuario  
**Para:** Entender su actividad  

**Prioridad:** Baja

**Criterios de aceptación:**
- Al hacer clic en usuario, se abre perfil detallado
- Muestra: info básica, perfil, estadísticas (favoritos, actividades vistas), historial reciente, fechas clave
- Botón volver al listado
- Se pueden realizar acciones desde el detalle

---

### HU-024: Validar Actividades Importadas (Admin)

**Como:** Administrador  
**Quiero:** Revisar y validar actividades importadas  
**Para:** Asegurar calidad de datos antes de publicar  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo rol "administrador" accede a /admin/validacion
- Muestra actividades "pendiente_validacion"
- Información completa en formato expandible
- Indica fuente de datos
- Acciones: aprobar, editar y aprobar, rechazar (con nota)
- Acciones en lote (selección múltiple)
- Filtro por fuente
- Conteo de pendientes
- Actividades procesadas desaparecen del listado
- Actividades rechazadas guardadas para auditoría

---

### HU-025: Ver Estado de Procesos ETL (Admin)

**Como:** Administrador  
**Quiero:** Ver estado de procesos ETL  
**Para:** Monitorear ingesta de datos  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo rol "administrador" accede a /admin/etl
- Info última ejecución: fecha/hora inicio/fin, duración, estado, totales (procesadas, exitosas, errores), lista de errores
- Lista de fuentes de datos con estado
- Próxima ejecución programada
- Historial de ejecuciones (tabla)
- Si proceso corriendo, se muestra en tiempo real
- Botón ver logs detallados

---

### HU-026: Ejecutar Proceso ETL Manual (Admin)

**Como:** Administrador  
**Quiero:** Ejecutar manualmente proceso ETL  
**Para:** Actualizar catálogo bajo demanda  

**Prioridad:** Media

**Criterios de aceptación:**
- Solo rol "administrador" puede ejecutar
- Botón "Ejecutar ETL" en página gestión ETL
- Verifica que no haya otro proceso corriendo
- Al confirmar, inicia proceso en background
- Notificación "Proceso iniciado"
- Redirección a vista de monitoreo en tiempo real
- Muestra: estado actual, progreso, logs
- Timeout 1 hora máximo
- Al finalizar, resumen completo
- Registro en tabla de ejecuciones

---

### HU-027: Ver Logs de Ejecución ETL (Admin)

**Como:** Administrador  
**Quiero:** Ver logs detallados de ejecución ETL  
**Para:** Diagnosticar problemas  

**Prioridad:** Baja

**Criterios de aceptación:**
- Desde historial, clic para ver logs
- Formato texto estructurado con: timestamp, nivel, mensaje, detalles (expandible)
- Filtro por nivel
- Búsqueda de mensajes específicos
- Errores destacados visualmente
- Descarga de log completo (.txt)
- Solo lectura

---

### HU-028: Configurar Fuentes de Datos ETL (Admin)

**Como:** Administrador  
**Quiero:** Configurar fuentes de datos ETL  
**Para:** Definir de dónde se obtienen actividades  

**Prioridad:** Baja

**Criterios de aceptación:**
- Solo rol "administrador" accede
- Página configuración fuentes ETL
- Se agregan: API REST, CSV público, JSON público
- Por fuente se configura: nombre, tipo, URL, credenciales, mapeo de campos, estado
- Prueba de conexión antes de guardar
- Fuentes editables o desactivables
- Solo fuentes activas se procesan
- Validación de URL accesible

---

### HU-029: Programar Ejecuciones ETL Automáticas (Admin)

**Como:** Administrador  
**Quiero:** Programar ejecuciones automáticas ETL  
**Para:** Mantener catálogo actualizado sin intervención  

**Prioridad:** Baja

**Criterios de aceptación:**
- Solo rol "administrador" accede
- Sección de programación en configuración ETL
- Configurable: frecuencia (diaria, semanal, mensual, cron), hora, días semana, zona horaria
- Muestra próxima ejecución calculada
- Activar/desactivar programación
- Editable
- Validación de conflictos
- Ejecuciones programadas en logs

---

## 7. Gestión de Ingesta (ETL)

### HU-030: Extractor de API IDRD

**Como:** Sistema  
**Quiero:** Extraer datos de actividades desde API IDRD  
**Para:** Incorporar oferta deportiva automáticamente  

**Prioridad:** Media

**Criterios de aceptación:**
- Script ETL se conecta a API IDRD
- Extrae actividades deportivas disponibles
- Maneja errores de conexión y timeout
- Logs detallados del proceso
- Datos extraídos pasan a transformer

---

### HU-031: Transformer de Datos ETL

**Como:** Sistema  
**Quiero:** Normalizar y transformar datos extraídos  
**Para:** Adaptarlos al modelo de datos de la plataforma  

**Prioridad:** Media

**Criterios de aceptación:**
- Transforma campos al formato interno
- Valida tipos de datos y formatos
- Normaliza fechas, coordenadas, texto
- Detecta y marca duplicados
- Genera logs de transformaciones
- Datos transformados pasan a loader

---

### HU-032: Loader de Datos ETL

**Como:** Sistema  
**Quiero:** Cargar datos transformados en la base de datos  
**Para:** Incorporarlos al catálogo de actividades  

**Prioridad:** Media

**Criterios de aceptación:**
- Inserta actividades en PostgreSQL
- Actividades insertadas con estado "pendiente_validacion"
- Maneja errores de inserción
- Previene duplicados
- Actualiza contadores (procesadas, exitosas, errores)
- Registra ejecución en tabla etl_executions

---

### HU-033: Reporte de Ejecución ETL

**Como:** Sistema  
**Quiero:** Generar reporte detallado de cada ejecución ETL  
**Para:** Proveer información a administradores  

**Prioridad:** Baja

**Criterios de aceptación:**
- Genera resumen con totales
- Lista detallada de errores
- Timestamp inicio/fin
- Estado final
- Logs completos guardados
- Reporte accesible desde panel admin

---

## 8. Dispositivos IoT

### HU-034: Vincular Dispositivo IoT

**Como:** Usuario registrado  
**Quiero:** Vincular un dispositivo IoT a mi cuenta  
**Para:** Sincronizar recomendaciones con el dispositivo físico  

**Prioridad:** Baja

**Criterios de aceptación:**
- Solo usuarios autenticados acceden
- Página /dispositivos con formulario de vinculación
- Usuario ingresa código único del dispositivo (ej: TRIQ-ABC123)
- Sistema valida que código existe y no está vinculado
- Se crea relación en tabla usuarios_dispositivos
- Se genera token JWT de dispositivo (válido 1 año)
- Se muestra información del dispositivo vinculado
- Botón para desvincular dispositivo
- Un dispositivo solo vinculado a un usuario a la vez

---

### HU-035: API de Sincronización para Dispositivo IoT

**Como:** Dispositivo IoT  
**Quiero:** Obtener recomendaciones del usuario vinculado  
**Para:** Mostrarlas en el dispositivo físico  

**Prioridad:** Baja

**Criterios de aceptación:**
- Endpoint GET /api/v1/iot/recommendations
- Autenticación con device_token (JWT)
- Sistema obtiene user_id asociado al dispositivo
- Genera recomendaciones usando algoritmo estándar
- Retorna top 3-5 recomendaciones
- Respuesta optimizada para display limitado: título (max 50 chars), fecha, localidad, tipo
- Incluye timestamp de última actualización
- Solo dispositivos vinculados y autenticados acceden
- Caché de 1 hora

---

## 📊 Resumen por Prioridad

| Prioridad | Cantidad | IDs |
|-----------|----------|-----|
| **Alta** | 16 historias | HU-001, HU-002, HU-004, HU-006, HU-007, HU-008, HU-009, HU-010, HU-011, HU-014, HU-015, HU-017, HU-020 |
| **Media** | 14 historias | HU-003, HU-005, HU-012, HU-013, HU-016, HU-018, HU-019, HU-021, HU-024, HU-025, HU-026, HU-030, HU-031, HU-032 |
| **Baja** | 5 historias | HU-022, HU-023, HU-027, HU-028, HU-029, HU-033, HU-034, HU-035 |

---

## 📈 Resumen por Módulo

| Módulo | Historias | Prioridad Alta | Prioridad Media | Prioridad Baja |
|--------|-----------|---------------|-----------------|----------------|
| Autenticación | 5 | 3 | 2 | 0 |
| Actividades | 8 | 6 | 2 | 0 |
| Favoritos | 3 | 2 | 1 | 0 |
| Recomendaciones | 2 | 1 | 1 | 0 |
| Perfil Usuario | 2 | 1 | 1 | 0 |
| Administración | 9 | 0 | 4 | 5 |
| ETL | 4 | 0 | 3 | 1 |
| IoT | 2 | 0 | 0 | 2 |

---

**Versión:** 1.0  
**Última actualización:** 21 de Octubre de 2025  
**Estado:** ✅ Aprobado para desarrollo
