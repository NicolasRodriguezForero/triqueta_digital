/**
 * API client configuration with axios interceptors.
 * Handles authentication tokens and error responses.
 */
import axios, { AxiosError, AxiosResponse, InternalAxiosRequestConfig } from "axios";

// Get API URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Request interceptor - Add auth token to requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("access_token");
    
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle token refresh and errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    
    // Don't try to refresh token for authentication endpoints (login, register, refresh)
    // These endpoints return 401/400 for invalid credentials, not expired tokens
    const isAuthEndpoint = originalRequest?.url?.includes("/auth/login") ||
                           originalRequest?.url?.includes("/auth/register") ||
                           originalRequest?.url?.includes("/auth/refresh");
    
    // If 401 and we haven't retried yet, try to refresh token
    // Only for non-auth endpoints (protected routes that need authentication)
    if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem("refresh_token");
      
      if (refreshToken) {
        try {
          // Try to refresh the access token
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          
          const { access_token, refresh_token: new_refresh_token } = response.data;
          
          // Save new tokens
          localStorage.setItem("access_token", access_token);
          localStorage.setItem("refresh_token", new_refresh_token);
          
          // Retry original request with new token
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
          }
          
          return apiClient(originalRequest);
        } catch (refreshError) {
          // Refresh failed, clear tokens and redirect to login
          // Only redirect if we're not already on login/register page
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          
          // Use router navigation instead of window.location to avoid full page reload
          // But only if not already on auth pages
          if (!window.location.pathname.includes("/login") && 
              !window.location.pathname.includes("/register")) {
            window.location.href = "/login";
          }
          
          return Promise.reject(refreshError);
        }
      } else {
        // No refresh token, redirect to login only if not already on auth pages
        if (!window.location.pathname.includes("/login") && 
            !window.location.pathname.includes("/register")) {
          window.location.href = "/login";
        }
      }
    }
    
    // For auth endpoints, just reject the error so it can be handled by the component
    // For other endpoints, also reject to allow error handling
    return Promise.reject(error);
  }
);

export default apiClient;
