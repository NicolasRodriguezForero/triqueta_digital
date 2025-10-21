/**
 * Authentication hooks using React Query
 */
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import * as authService from "../services/auth";
import type { LoginData, RegisterData } from "../services/auth";

/**
 * Hook to get current user
 */
export function useCurrentUser() {
  return useQuery({
    queryKey: ["currentUser"],
    queryFn: authService.getCurrentUser,
    enabled: authService.isAuthenticated(),
    retry: false,
  });
}

/**
 * Hook to register a new user
 */
export function useRegister() {
  const navigate = useNavigate();
  
  return useMutation({
    mutationFn: (data: RegisterData) => authService.register(data),
    onSuccess: () => {
      navigate({ to: "/login" });
    },
  });
}

/**
 * Hook to login
 */
export function useLogin() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  
  return useMutation({
    mutationFn: (data: LoginData) => authService.login(data),
    onSuccess: () => {
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
      navigate({ to: "/" });
    },
  });
}

/**
 * Hook to logout
 */
export function useLogout() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  
  return useMutation({
    mutationFn: authService.logout,
    onSuccess: () => {
      // Clear all queries
      queryClient.clear();
      navigate({ to: "/login" });
    },
  });
}

/**
 * Check if user is authenticated
 */
export function useIsAuthenticated(): boolean {
  return authService.isAuthenticated();
}
