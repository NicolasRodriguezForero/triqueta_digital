/**
 * Authentication hooks integrating AuthContext with React Query
 */
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { useAuth as useAuthContext } from "../contexts/AuthContext";
import type { LoginData, RegisterData } from "../services/auth";

/**
 * Re-export the main auth hook from context
 */
export { useAuth } from "../contexts/AuthContext";

/**
 * Hook to get current user (directly from context)
 */
export function useCurrentUser() {
  const { user, isLoading } = useAuthContext();
  return {
    data: user,
    isLoading,
    isError: !user && !isLoading,
  };
}

/**
 * Hook to register a new user (React Query style wrapper)
 * Auto-login after successful registration
 */
export function useRegister() {
  const { register, login } = useAuthContext();
  const navigate = useNavigate();
  
  return useMutation({
    mutationFn: async (data: RegisterData) => {
      // Register user
      await register(data);
      // Auto-login after registration
      await login({
        email: data.email,
        password: data.password,
      });
    },
    onSuccess: () => {
      // Navigate to home after successful registration and auto-login
      navigate({ to: "/" });
    },
  });
}

/**
 * Hook to login (React Query style wrapper)
 */
export function useLogin() {
  const { login } = useAuthContext();
  const navigate = useNavigate();
  
  return useMutation({
    mutationFn: (data: LoginData) => login(data),
    onSuccess: () => {
      // Navigate to home after successful login
      navigate({ to: "/" });
    },
  });
}

/**
 * Hook to logout (React Query style wrapper)
 */
export function useLogout() {
  const { logout } = useAuthContext();
  const navigate = useNavigate();
  
  return useMutation({
    mutationFn: () => logout(),
    onSuccess: () => {
      // Navigate to login after logout
      navigate({ to: "/login" });
    },
  });
}

/**
 * Check if user is authenticated
 */
export function useIsAuthenticated(): boolean {
  const { isAuthenticated } = useAuthContext();
  return isAuthenticated;
}
