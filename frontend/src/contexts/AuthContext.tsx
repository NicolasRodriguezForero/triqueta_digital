/**
 * Authentication Context
 * Manages global authentication state, user session, and token handling.
 */
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import * as authService from "../services/auth";
import type { Usuario, LoginData, RegisterData } from "../services/auth";

interface AuthContextType {
  user: Usuario | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (data: LoginData) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * AuthProvider component
 * Wraps the application and provides authentication context.
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<Usuario | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && authService.isAuthenticated();

  /**
   * Initialize authentication state on mount
   * Checks if there's a valid token and fetches user data
   */
  useEffect(() => {
    const initAuth = async () => {
      try {
        const hasToken = authService.isAuthenticated();
        
        if (hasToken) {
          // Try to fetch current user
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        }
      } catch (error) {
        console.error("Failed to initialize auth:", error);
        // Clear invalid tokens
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  /**
   * Login user with email and password
   */
  const login = async (data: LoginData) => {
    try {
      setIsLoading(true);
      
      // Call login service (stores tokens in localStorage)
      await authService.login(data);
      
      // Fetch user data
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Register a new user
   */
  const register = async (data: RegisterData) => {
    try {
      setIsLoading(true);
      
      // Register user
      await authService.register(data);
    } catch (error) {
      console.error("Registration failed:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Logout user and clear session
   */
  const logout = async () => {
    try {
      setIsLoading(true);
      
      // Call logout service (revokes refresh token)
      await authService.logout();
      
      // Clear user state
      setUser(null);
    } catch (error) {
      console.error("Logout failed:", error);
      // Even if logout fails, clear local state
      setUser(null);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Refresh user data (useful after profile updates)
   */
  const refreshUser = async () => {
    try {
      if (!authService.isAuthenticated()) {
        return;
      }
      
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.error("Failed to refresh user:", error);
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Custom hook to use authentication context
 * @throws Error if used outside AuthProvider
 */
export function useAuth() {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  
  return context;
}
