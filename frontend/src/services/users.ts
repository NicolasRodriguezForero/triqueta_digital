/**
 * User service for profile management.
 */
import apiClient from "./api";
import { Usuario, PerfilUsuario } from "./auth";

export interface PerfilUsuarioUpdate {
  nombre_completo?: string;
  telefono?: string;
  biografia?: string;
  etiquetas_interes?: string[];
  localidad_preferida?: string;
  disponibilidad_horaria?: string;
  nivel_actividad?: string;
}

/**
 * Get current user profile with all information
 */
export const getMyProfile = async (): Promise<Usuario> => {
  const response = await apiClient.get<Usuario>("/users/me");
  return response.data;
};

/**
 * Update current user profile
 */
export const updateMyProfile = async (data: PerfilUsuarioUpdate): Promise<PerfilUsuario> => {
  const response = await apiClient.put<PerfilUsuario>("/users/me/profile", data);
  return response.data;
};

/**
 * Delete current user account
 */
export const deleteMyAccount = async (): Promise<void> => {
  await apiClient.delete("/users/me");
};

/**
 * Get user by ID
 */
export const getUserById = async (userId: number): Promise<Usuario> => {
  const response = await apiClient.get<Usuario>(`/users/${userId}`);
  return response.data;
};
