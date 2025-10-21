/**
 * Authentication service for login, register, and token management.
 */
import apiClient from "./api";

export interface RegisterData {
  email: string;
  password: string;
  nombre_completo?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Usuario {
  id: number;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
  perfil?: PerfilUsuario | null;
}

export interface PerfilUsuario {
  id: number;
  usuario_id: number;
  nombre_completo?: string | null;
  telefono?: string | null;
  biografia?: string | null;
  etiquetas_interes: string[];
  localidad_preferida?: string | null;
  disponibilidad_horaria?: string | null;
  nivel_actividad?: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Register a new user
 */
export const register = async (data: RegisterData): Promise<Usuario> => {
  const response = await apiClient.post<Usuario>("/auth/register", data);
  return response.data;
};

/**
 * Login with email and password
 */
export const login = async (data: LoginData): Promise<TokenResponse> => {
  const response = await apiClient.post<TokenResponse>("/auth/login", data);
  
  // Save tokens to localStorage
  localStorage.setItem("access_token", response.data.access_token);
  localStorage.setItem("refresh_token", response.data.refresh_token);
  
  return response.data;
};

/**
 * Logout user
 */
export const logout = async (): Promise<void> => {
  const refreshToken = localStorage.getItem("refresh_token");
  
  if (refreshToken) {
    try {
      await apiClient.post("/auth/logout", {
        refresh_token: refreshToken,
      });
    } catch (error) {
      console.error("Logout error:", error);
    }
  }
  
  // Clear tokens from localStorage
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

/**
 * Get current user information
 */
export const getCurrentUser = async (): Promise<Usuario> => {
  const response = await apiClient.get<Usuario>("/auth/me");
  return response.data;
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem("access_token");
};
