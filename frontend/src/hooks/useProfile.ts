/**
 * User profile hooks using React Query
 */
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import * as userService from "../services/users";
import type { PerfilUsuarioUpdate } from "../services/users";
import { useAuth } from "../contexts/AuthContext";

/**
 * Hook to get user profile
 */
export function useProfile() {
  return useQuery({
    queryKey: ["profile"],
    queryFn: userService.getMyProfile,
  });
}

/**
 * Hook to update user profile
 */
export function useUpdateProfile() {
  const queryClient = useQueryClient();
  const { refreshUser } = useAuth();
  
  return useMutation({
    mutationFn: (data: PerfilUsuarioUpdate) => userService.updateMyProfile(data),
    onSuccess: async () => {
      // Invalidate and refetch profile data
      queryClient.invalidateQueries({ queryKey: ["profile"] });
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
      
      // Also refresh user in AuthContext
      await refreshUser();
    },
  });
}

/**
 * Hook to delete user account
 */
export function useDeleteAccount() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: userService.deleteMyAccount,
    onSuccess: () => {
      // Clear all queries and redirect to home
      queryClient.clear();
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/";
    },
  });
}
