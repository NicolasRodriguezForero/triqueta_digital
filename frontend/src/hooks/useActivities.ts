/**
 * React Query hooks for activities management
 */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import {
  getActivities,
  getActivityById,
  createActivity,
  updateActivity,
  deleteActivity,
  registerActivityView,
  type ActividadFilters,
  type ActividadCreate,
  type ActividadUpdate,
} from "../services/activities";

// Query keys for cache management
export const activityKeys = {
  all: ["activities"] as const,
  lists: () => [...activityKeys.all, "list"] as const,
  list: (filters?: ActividadFilters) => [...activityKeys.lists(), filters] as const,
  details: () => [...activityKeys.all, "detail"] as const,
  detail: (id: string) => [...activityKeys.details(), id] as const,
};

/**
 * Hook to fetch list of activities with filters (RF-007, RF-008)
 */
export function useActivities(filters?: ActividadFilters) {
  return useQuery({
    queryKey: activityKeys.list(filters),
    queryFn: () => getActivities(filters),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook to fetch a single activity by ID (RF-010)
 */
export function useActivity(id: string, enabled = true) {
  return useQuery({
    queryKey: activityKeys.detail(id),
    queryFn: async () => {
      const activity = await getActivityById(id);
      // Register view after fetching (don't await to avoid blocking)
      registerActivityView(id).catch(console.error);
      return activity;
    },
    enabled: enabled && !!id,
    staleTime: 1000 * 60 * 10, // 10 minutes
  });
}

/**
 * Hook to create a new activity (RF-009) - Admin only
 */
export function useCreateActivity() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (data: ActividadCreate) => createActivity(data),
    onSuccess: (newActivity) => {
      // Invalidate activities list to refetch
      queryClient.invalidateQueries({ queryKey: activityKeys.lists() });
      // Navigate to the new activity detail page
      navigate({ to: `/actividades/${newActivity.id}` });
    },
  });
}

/**
 * Hook to update an existing activity (RF-009) - Admin only
 */
export function useUpdateActivity(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ActividadUpdate) => updateActivity(id, data),
    onSuccess: (updatedActivity) => {
      // Update the specific activity in cache
      queryClient.setQueryData(activityKeys.detail(id), updatedActivity);
      // Invalidate lists to refetch
      queryClient.invalidateQueries({ queryKey: activityKeys.lists() });
    },
  });
}

/**
 * Hook to delete an activity (RF-009) - Admin only
 */
export function useDeleteActivity() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (id: string) => deleteActivity(id),
    onSuccess: (_, id) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: activityKeys.detail(id) });
      // Invalidate lists to refetch
      queryClient.invalidateQueries({ queryKey: activityKeys.lists() });
      // Navigate back to activities list
      navigate({ to: "/actividades" });
    },
  });
}

/**
 * Hook to manually register an activity view
 * (already called automatically in useActivity)
 */
export function useRegisterView() {
  return useMutation({
    mutationFn: (id: string) => registerActivityView(id),
  });
}
