# Prompt para Generación de Wireframes - Triqueta Digital

## Contexto del Proyecto

**Triqueta Digital** es una plataforma web que conecta actividades culturales, recreativas y deportivas en las localidades de **Chapinero, Santa Fe y La Candelaria** (Bogotá, Colombia). El objetivo es integrar al menos el 70% de la oferta disponible y proveer recomendaciones personalizadas mediante IA.

---

## Solicitud para la IA

Necesito que generes wireframes completos para una aplicación web responsive (desktop y móvil) con las siguientes características:

### 1. Información General de la Aplicación

**Nombre:** Triqueta Digital  
**Tipo:** Plataforma web responsive (SPA/PWA)  
**Usuarios objetivo:** Ciudadanos de Bogotá (localidades Chapinero, Santa Fe, La Candelaria) y administradores  
**Propósito:** Descubrir, explorar y recibir recomendaciones personalizadas de actividades culturales, deportivas y recreativas

---

### 2. Stack Tecnológico (para contexto de diseño)

- **Frontend:** React 18+ con Vite, TypeScript, TailwindCSS, Shadcn UI
- **Estilo visual:** Moderno, limpio, accesible (WCAG 2.1 AA)
- **Componentes:** Cards, Sheets/Drawers, Badges, Buttons, Forms, Dialogs
- **Navegación:** Navbar responsive con menú hamburguesa en móvil

---

### 3. Actores del Sistema

1. **Usuario no autenticado:** Puede explorar y buscar actividades
2. **Usuario autenticado:** Acceso completo a favoritos, recomendaciones y perfil
3. **Administrador:** Gestión de actividades, importación de datos, dashboard

---

### 4. Páginas y Vistas Principales a Diseñar

#### 4.1 Página de Inicio / Landing
- **Elementos:**
  - Hero section con título llamativo y CTA (Call To Action)
  - Breve descripción del propósito de la plataforma
  - Sección de actividades destacadas (3-4 cards)
  - Botones: "Explorar Actividades", "Iniciar Sesión", "Registrarse"
- **Responsive:** Hero apilado en móvil, grid de 2 columnas en tablet, 4 en desktop

#### 4.2 Registro de Usuario
- **Elementos:**
  - Formulario centrado con campos:
    - Email (validación de formato)
    - Contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número, 1 especial)
    - Confirmación de contraseña
    - Nombre completo
    - Checkbox: Aceptar términos y condiciones
  - Botón "Registrarse"
  - Link: "¿Ya tienes cuenta? Inicia sesión"
  - Mensajes de error descriptivos bajo cada campo
- **Responsive:** Formulario de ancho completo en móvil, max-width en desktop

#### 4.3 Inicio de Sesión
- **Elementos:**
  - Formulario centrado con campos:
    - Email
    - Contraseña
  - Botón "Iniciar Sesión"
  - Links: "¿Olvidaste tu contraseña?" y "Crear cuenta"
  - Mensaje de error genérico para credenciales incorrectas
- **Responsive:** Similar a registro

#### 4.4 Exploración de Actividades (Página Principal)
- **Elementos:**
  - **Navbar superior:**
    - Logo Triqueta Digital (izquierda)
    - Barra de búsqueda central (con icono de lupa)
    - Botones: "Favoritos", "Perfil", "Cerrar Sesión" (derecha)
    - En móvil: Logo + menú hamburguesa
  - **Filtros laterales (desktop) / Sheet (móvil):**
    - Tipo de actividad (dropdown/select)
    - Localidad (Chapinero, Santa Fe, La Candelaria)
    - Rango de fechas (date picker)
    - Precio (slider o checkbox "Solo gratuitas")
    - Nivel de actividad (Bajo, Medio, Alto)
    - Etiquetas (chips seleccionables: cultura, deporte, recreación, etc.)
    - Botón "Aplicar Filtros" y "Limpiar Filtros"
  - **Grid de actividades:**
    - Tarjetas (cards) en grid responsive (1 col móvil, 2 tablet, 3-4 desktop)
    - Cada card muestra:
      - Imagen de la actividad (placeholder si no hay)
      - Título
      - Localidad (badge)
      - Tipo (badge)
      - Fecha y hora
      - Precio (o badge "Gratis")
      - Etiquetas (2-3 chips pequeños)
      - Icono de favorito (corazón)
      - Botón "Ver Detalle"
  - **Paginación:** Botones "Anterior" / "Siguiente" + indicador de página
  - **Contador:** "Mostrando X de Y actividades"
- **Responsive:** Filtros en sidebar fijo (desktop), en sheet/drawer (móvil)

#### 4.5 Detalle de Actividad
- **Elementos:**
  - Breadcrumb: Inicio > Actividades > [Nombre actividad]
  - Imagen principal (grande, hero)
  - Título de la actividad
  - Badges: Localidad, Tipo, Nivel
  - Descripción completa (texto largo)
  - Información clave:
    - Fecha y hora
    - Ubicación (dirección + mapa embebido)
    - Precio
    - Contacto (email, teléfono, sitio web)
  - Etiquetas completas (chips)
  - Botón "Guardar en Favoritos" (destacado)
  - Botón "Compartir"
  - Sección "Actividades Similares" (3 cards pequeñas)
- **Responsive:** Layout de 1 columna en móvil, 2 columnas en desktop (info + mapa)

#### 4.6 Mis Favoritos
- **Elementos:**
  - Título: "Mis Actividades Favoritas"
  - Grid de cards similar a exploración
  - Cada card tiene botón "Eliminar de Favoritos" (icono X)
  - Mensaje si no hay favoritos: "Aún no has guardado actividades"
- **Responsive:** Grid responsive igual que exploración

#### 4.7 Recomendaciones Personalizadas
- **Elementos:**
  - Título: "Recomendaciones para ti"
  - Subtítulo explicativo: "Basadas en tus intereses y actividades guardadas"
  - Grid de cards de actividades recomendadas
  - Cada card incluye badge "Recomendado" y texto breve de explicación:
    - "Por tus intereses en cultura"
    - "Popular en tu localidad"
    - "Coincide con tu disponibilidad"
  - Botón "Ver más recomendaciones"
- **Responsive:** Grid responsive

#### 4.8 Perfil de Usuario
- **Elementos:**
  - Foto de perfil (circular, con opción de cambiar)
  - Nombre completo (editable)
  - Email (no editable)
  - Sección "Mis Intereses":
    - Chips seleccionables: Cultura, Deporte, Recreación, Arte, Música, etc.
  - Sección "Disponibilidad":
    - Días de la semana (checkboxes)
    - Horarios preferidos (mañana, tarde, noche)
  - Sección "Localidad Preferida":
    - Dropdown: Chapinero, Santa Fe, La Candelaria, Todas
  - Botón "Guardar Cambios"
  - Botón "Cambiar Contraseña"
- **Responsive:** Formulario de 1 columna en móvil, 2 columnas en desktop

#### 4.9 Panel Administrativo - Dashboard
- **Elementos:**
  - Sidebar de navegación (desktop) / Drawer (móvil):
    - Dashboard
    - Gestión de Actividades
    - Importar Actividades
    - Gestión ETL
    - Usuarios (opcional)
  - **Vista Dashboard:**
    - Cards con métricas clave:
      - Total de actividades
      - Usuarios activos
      - Actividades más vistas
      - Tasa de conversión de recomendaciones
    - Gráficos simples (barras, líneas)
    - Tabla de actividades recientes
- **Responsive:** Sidebar colapsable en tablet, drawer en móvil

#### 4.10 Panel Administrativo - Gestión de Actividades
- **Elementos:**
  - Botón "Crear Nueva Actividad" (destacado)
  - Tabla de actividades con columnas:
    - Título
    - Tipo
    - Localidad
    - Fecha
    - Estado (Activa, Inactiva)
    - Acciones (Editar, Eliminar)
  - Filtros rápidos: Estado, Tipo, Localidad
  - Búsqueda por título
  - Paginación
- **Responsive:** Tabla scrollable horizontal en móvil, cards en lugar de tabla

#### 4.11 Panel Administrativo - Formulario de Actividad
- **Elementos:**
  - Título: "Crear/Editar Actividad"
  - Formulario con campos:
    - Título (text)
    - Descripción (textarea)
    - Tipo (select)
    - Localidad (select)
    - Fecha de inicio (date picker)
    - Fecha de fin (date picker)
    - Horario (time picker)
    - Ubicación (text + mapa para seleccionar coordenadas)
    - Precio (number, con checkbox "Gratis")
    - Nivel de actividad (select)
    - Etiquetas (input con chips)
    - Imagen (upload)
    - Contacto (email, teléfono, sitio web)
  - Botones: "Guardar", "Cancelar"
- **Responsive:** Formulario de 1 columna en móvil, 2 columnas en desktop

#### 4.12 Panel Administrativo - Importación de Actividades
- **Elementos:**
  - Título: "Importar Actividades"
  - Área de drag & drop para archivos CSV/JSON
  - Botón "Seleccionar Archivo"
  - Preview de datos importados (tabla)
  - Indicadores de validación:
    - Actividades válidas (verde)
    - Actividades con errores (rojo)
    - Duplicados detectados (amarillo)
  - Botón "Confirmar Importación"
  - Log de resultados
- **Responsive:** Área de drop apilada en móvil

---

### 5. Componentes Clave a Incluir

1. **ActivityCard:** Card con imagen, título, badges, precio, botón favorito
2. **Navbar:** Logo, búsqueda, menú usuario, responsive
3. **FilterPanel:** Sidebar con filtros múltiples
4. **SearchBar:** Input con icono de búsqueda y sugerencias
5. **Badge:** Pequeño, colores diferenciados por tipo
6. **Button:** Primario, secundario, outline, con iconos
7. **Dialog/Modal:** Para confirmaciones y formularios
8. **Sheet/Drawer:** Para filtros en móvil
9. **Pagination:** Botones + indicador de página
10. **Form:** Inputs, selects, date pickers, textareas

---

### 6. Paleta de Colores Sugerida

- **Primario:** Azul vibrante (#3B82F6) - para CTAs y elementos destacados
- **Secundario:** Verde (#10B981) - para badges de "Gratis" y estados positivos
- **Acento:** Naranja (#F59E0B) - para notificaciones y alertas
- **Neutros:** Grises (#F3F4F6, #6B7280, #1F2937) - para fondos, textos y bordes
- **Error:** Rojo (#EF4444)
- **Éxito:** Verde (#10B981)

---

### 7. Consideraciones de UX/UI

- **Accesibilidad:** Contraste WCAG 2.1 AA, labels en formularios, navegación por teclado
- **Responsive:** Mobile-first, breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- **Feedback visual:** Loaders, skeletons, mensajes de éxito/error, estados hover/active
- **Navegación clara:** Breadcrumbs, navbar fija, indicadores de página actual
- **Imágenes:** Placeholders cuando no hay imagen, lazy loading
- **Microinteracciones:** Animaciones sutiles en botones, transiciones suaves

---

### 8. Flujos de Usuario Principales

1. **Usuario nuevo:**
   - Landing → Registro → Exploración → Ver detalle → Guardar favorito
2. **Usuario recurrente:**
   - Login → Recomendaciones → Ver detalle → Guardar favorito
3. **Búsqueda específica:**
   - Exploración → Aplicar filtros → Buscar → Ver detalle
4. **Administrador:**
   - Login → Dashboard → Crear actividad → Guardar

---

### 9. Formato de Entrega Esperado

Por favor, genera wireframes que incluyan:

1. **Vista desktop** (1280px+) para cada página principal
2. **Vista móvil** (375px) para páginas clave (exploración, detalle, perfil)
3. **Anotaciones** que expliquen:
   - Interacciones (hover, click, scroll)
   - Estados (loading, error, vacío)
   - Comportamiento responsive
4. **Jerarquía visual clara:** Títulos, subtítulos, cuerpo de texto
5. **Espaciado consistente:** Padding, margins, gaps
6. **Iconografía:** Indicar iconos necesarios (lupa, corazón, menú, etc.)

---

### 10. Prioridad de Páginas

**Alta prioridad (MVP Core):**
- Exploración de Actividades
- Detalle de Actividad
- Registro/Login
- Mis Favoritos
- Perfil de Usuario

**Media prioridad:**
- Recomendaciones Personalizadas
- Dashboard Administrativo
- Gestión de Actividades

**Baja prioridad:**
- Importación de Actividades
- Gestión ETL

---

## Notas Adicionales

- La aplicación debe sentirse **moderna, limpia y fácil de usar**
- Inspiración visual: Plataformas como Eventbrite, Meetup, pero con enfoque local y cultural
- El diseño debe transmitir **comunidad, cultura y conexión con el territorio**
- Considerar **inclusividad** en imágenes y lenguaje
- La experiencia móvil es **crítica** (70% de usuarios esperados en móvil)

---

## Contexto Técnico Adicional

**Modelo de datos clave:**
- **Actividad:** id, título, descripción, tipo, localidad, fecha_inicio, fecha_fin, ubicación (lat/lng), precio, nivel, etiquetas, imagen_url, contacto
- **Usuario:** id, email, nombre, foto, intereses, disponibilidad, localidad_preferida
- **Favorito:** usuario_id, actividad_id, fecha_guardado

**Tipos de actividad:** Cultural, Deportiva, Recreativa, Artística, Musical, Gastronómica, Educativa
**Localidades:** Chapinero, Santa Fe, La Candelaria
**Niveles:** Bajo, Medio, Alto

---

**¿Estás listo para generar los wireframes?** Por favor, comienza con las páginas de alta prioridad y asegúrate de incluir tanto vistas desktop como móviles para cada una.
