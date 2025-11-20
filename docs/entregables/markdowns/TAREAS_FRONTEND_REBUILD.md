# Plan de Rebuild Frontend Triqueta Digital

> Alcance: reconstrucción completa del frontend desde cero, alineada con el cronograma general. Incluye setup inicial, páginas, componentes, hooks, pruebas y optimizaciones finales.

## 1. Setup Inicial (Semana 1)

- Crear proyecto React 19 con Vite + TypeScript.
- Configurar linting/prettier según convenciones (ESLint strict, Prettier, Husky opcional).
- Integrar TailwindCSS y Shadcn UI (instalación, estilos base, configuración).
- Configurar TanStack Router y React Query con estructura modular.
- Implementar Axios con interceptors para manejo de tokens.
- Crear layout base (Navbar, Footer, Layout principal) y componentes UI reutilizables (Button, Input, Card, Modal, Badge, Alert, Loading states).
- Configurar theming y variables de Tailwind.
- Configurar testing: Vitest + Testing Library + Playwright base.

## 2. Autenticación y Usuarios (Sprint 1)

- Implementar contexto de autenticación (AuthContext) con persistencia y refresco de tokens.
- Páginas `/register`, `/login`, `/profile` con formularios, validaciones y estados de carga/errores.
- Protected routes con TanStack Router (guardias, redirects, roles admin/user).
- Interceptor Axios para refresco automático de tokens y manejo de expiraciones.
- Componentes de formularios reutilizables (Input, PasswordInput, Checkbox, FormField, ErrorMessage).
- Hooks: `useAuth`, `useLogin`, `useRegister`, `useProfile`, `useUpdateProfile`.
- Tests unitarios de hooks y componentes clave; pruebas de integración de flujo register/login/profile.

## 3. Catálogo de Actividades Parte 1 (Sprint 2)

- Servicio API `activities.ts` con tipado completo.
- Hooks React Query: `useActivities`, `useActivity`, `usePaginatedActivities`.
- Componentes: `ActivityCard`, `SearchBar`, `ActivityList`, `PaginationControls`.
- Página `/actividades` con filtros básicos (palabra clave, tipo, localidad) y paginación.
- Página `/actividades/$id` con detalle, mapa/ubicación (si aplica), etiquetas y contenido expandible.
- Estados de carga y error con placeholders skeleton.
- Testing: unit tests para componentes, hooks, y pruebas de integración para flujo de búsqueda/detalle.

## 4. Catálogo de Actividades Parte 2 + Admin (Sprint 3)

- Página `/admin/actividades` con tabla de gestión, ordenamiento, paginación interna.
- Formularios `ActivityForm` para crear/editar (con validaciones dinámicas, carga de etiquetas, localización).
- Hooks: `useCreateActivity`, `useUpdateActivity`, `useDeleteActivity`, `useUploadActivities`.
- Componente `ActivityFilters` tipo sheet con todos los filtros avanzados (fechas, gratis, nivel, etiquetas, localidad, tipo, estado).
- Implementación de subida de archivos CSV/JSON con feedback visual (resumen, errores, progreso).
- UI de estados de actividades (badges: activa, pendiente_validacion, rechazada).
- Testing unitario y E2E del CRUD admin completo y del flujo de importación.

## 5. Favoritos y Recomendaciones (Sprint 4)

- Servicios API `favorites.ts` y `recommendations.ts`.
- Hooks React Query: `useFavorites`, `useAddFavorite`, `useRemoveFavorite`, `useRecommendations`.
- Componente `FavoriteButton` con control de estado optimista (optimistic updates).
- Integración de `FavoriteButton` en `ActivityCard` (listados y detalle).
- Página `/favoritos` mostrando lista, filtros básicos y estados vacíos.
- Página `/recomendaciones` con tarjetas explicativas y motivos personalizados.
- Componente de explicación (tooltips o acordeones) para recomendaciones.
- Tests unitarios de hooks/componentes y E2E del flujo favoritos/recomendaciones.

## 6. Dashboard Admin y Gestión Usuarios (Sprint 5)

- Página `/admin/dashboard` con layout responsivo, cards de métricas y gráficos (Recharts).
- Gráficos: pastel actividades por localidad, barras actividades por tipo, listas TOP 10.
- Componentes `MetricCard`, `TrendIndicator`, `ChartContainer`.
- Página `/admin/usuarios` con tabla, filtros, acciones (cambio de rol/estado) y confirmaciones.
- Hooks: `useAdminDashboard`, `useAdminUsers`, `useUpdateUserRole`, `useUpdateUserStatus`.
- Gestión de caché React Query (invalidation, stale time) para datos admin.
- Tests unitarios e integración de dashboards y gestión de usuarios.

## 7. ETL & Validación de Actividades (Sprint 6)

- Página `/admin/etl` con estado actual, trigger manual de ejecución y streaming de logs (SSE/polling).
- Componente `LogViewer` con autoscroll y filtros.
- Indicadores de progreso y estados (éxito, error, en ejecución).
- Página `/admin/validacion` para actividades pendientes: lista, detalles expandibles, acciones aprobar/editar y aprobar/rechazar.
- Formularios rápidos para editar campos antes de aprobar.
- Hooks: `useEtlStatus`, `useRunEtl`, `useEtlLogs`, `usePendingActivities`, `useApproveActivity`, `useRejectActivity`.
- Tests unitarios y E2E del flujo ETL + validación admin.

## 8. Optimización Final, Accesibilidad y Deploy (Sprint 7)

- Revisar y optimizar code splitting, lazy loading de rutas y componentes pesados.
- Implementar lazy loading de imágenes y placeholders.
- Auditar accesibilidad (WCAG 2.1 AA): roles ARIA, foco, contrastes, navegación teclado.
- Testing cross-browser (Chrome, Firefox, Safari, Edge) y responsive (desktop, tablet, mobile).
- Lighthouse audits (Performance >90 desktop, >80 mobile; Accessibility >95).
- Tests E2E completos con Playwright + smoke tests previos a deploy.
- Integración con pipeline CI/CD (scripts de build/test, reportes).
- Actualización y publicación de documentación frontend (Storybook/guía de componentes, README).
- Preparar assets para demo final y capturas.

## 9. Actividades Transversales

- Mantener backlog frontend actualizado (issues, prioridades) en conjunto con PM.
- Asistir a dailies, refinamientos y retrospectivas.
- Coordinar con backend para contract testing (OpenAPI, DTOs, mocks).
- Soporte continuo ante bugs detectados en QA/producción.
- Revisar pull requests y realizar code reviews cruzadas.
