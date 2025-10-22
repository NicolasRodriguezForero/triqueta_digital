/**
 * Activities service for cultural, recreational and sports activities.
 * Implements requirements RF-006 to RF-010 from SRS.
 */
import apiClient from "./api";

// Activity types
export type TipoActividad = "cultura" | "deporte" | "recreacion";
export type Localidad = "Chapinero" | "Santa Fe" | "La Candelaria";
export type NivelActividad = "bajo" | "medio" | "alto";
export type EstadoActividad = "activa" | "pendiente_validacion" | "rechazada" | "inactiva";
export type FuenteActividad = "manual" | "idrd" | "api" | "csv";

export interface Actividad {
  id: string;
  titulo: string;
  descripcion: string;
  tipo: TipoActividad;
  fecha_inicio: string;
  fecha_fin?: string | null;
  ubicacion_direccion: string;
  ubicacion_lat: number;
  ubicacion_lng: number;
  localidad: Localidad;
  precio: number;
  es_gratis: boolean;
  nivel_actividad?: NivelActividad | null;
  etiquetas: string[];
  contacto?: string | null;
  enlace_externo?: string | null;
  fuente: FuenteActividad;
  estado: EstadoActividad;
  popularidad_favoritos: number;
  popularidad_vistas: number;
  popularidad_normalizada: number;
  imagen_url?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ActividadCreate {
  titulo: string;
  descripcion: string;
  tipo: TipoActividad;
  fecha_inicio: string;
  fecha_fin?: string | null;
  ubicacion_direccion: string;
  ubicacion_lat: number;
  ubicacion_lng: number;
  localidad: Localidad;
  precio?: number;
  es_gratis?: boolean;
  nivel_actividad?: NivelActividad | null;
  etiquetas: string[];
  contacto?: string | null;
  enlace_externo?: string | null;
  imagen_url?: string | null;
}

export interface ActividadUpdate {
  titulo?: string;
  descripcion?: string;
  tipo?: TipoActividad;
  fecha_inicio?: string;
  fecha_fin?: string | null;
  ubicacion_direccion?: string;
  ubicacion_lat?: number;
  ubicacion_lng?: number;
  localidad?: Localidad;
  precio?: number;
  es_gratis?: boolean;
  nivel_actividad?: NivelActividad | null;
  etiquetas?: string[];
  contacto?: string | null;
  enlace_externo?: string | null;
  estado?: EstadoActividad;
  imagen_url?: string | null;
}

export interface ActividadFilters {
  tipo?: TipoActividad;
  localidad?: Localidad;
  es_gratis?: boolean;
  nivel_actividad?: NivelActividad;
  fecha_desde?: string;
  fecha_hasta?: string;
  etiquetas?: string[];
  q?: string; // Search query
  skip?: number;
  limit?: number;
}

export interface PaginationInfo {
  total: number;
  skip: number;
  limit: number;
  has_more: boolean;
}

export interface ActividadListResponse {
  data: Actividad[];
  pagination: PaginationInfo;
}

/**
 * Get list of activities with filters and pagination (RF-007)
 */
export const getActivities = async (filters?: ActividadFilters): Promise<ActividadListResponse> => {
  const params = new URLSearchParams();
  
  if (filters) {
    if (filters.tipo) params.append("tipo", filters.tipo);
    if (filters.localidad) params.append("localidad", filters.localidad);
    if (filters.es_gratis !== undefined) params.append("es_gratis", String(filters.es_gratis));
    if (filters.nivel_actividad) params.append("nivel_actividad", filters.nivel_actividad);
    if (filters.fecha_desde) params.append("fecha_desde", filters.fecha_desde);
    if (filters.fecha_hasta) params.append("fecha_hasta", filters.fecha_hasta);
    if (filters.etiquetas && filters.etiquetas.length > 0) {
      filters.etiquetas.forEach(tag => params.append("etiquetas", tag));
    }
    if (filters.q) params.append("q", filters.q);
    if (filters.skip !== undefined) params.append("skip", String(filters.skip));
    if (filters.limit !== undefined) params.append("limit", String(filters.limit));
  }
  
  const response = await apiClient.get<ActividadListResponse>(
    `/actividades?${params.toString()}`
  );
  return response.data;
};

/**
 * Get activity by ID (RF-010)
 */
export const getActivityById = async (id: string): Promise<Actividad> => {
  const response = await apiClient.get<Actividad>(`/actividades/${id}`);
  return response.data;
};

/**
 * Create new activity (RF-009) - Admin only
 */
export const createActivity = async (data: ActividadCreate): Promise<Actividad> => {
  const response = await apiClient.post<Actividad>("/actividades", data);
  return response.data;
};

/**
 * Update activity (RF-009) - Admin only
 */
export const updateActivity = async (
  id: string,
  data: ActividadUpdate
): Promise<Actividad> => {
  const response = await apiClient.put<Actividad>(`/actividades/${id}`, data);
  return response.data;
};

/**
 * Delete activity (RF-009) - Admin only
 */
export const deleteActivity = async (id: string): Promise<void> => {
  await apiClient.delete(`/actividades/${id}`);
};

/**
 * Register activity view to increase popularity
 */
export const registerActivityView = async (id: string): Promise<void> => {
  await apiClient.post(`/actividades/${id}/view`);
};
