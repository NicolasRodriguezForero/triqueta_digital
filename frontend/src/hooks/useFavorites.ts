/**
 * React Query hooks for favorites functionality
 */
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import * as favoritesApi from "../services/favorites";

/**
 * Query key factory for favorites
 */
export const favoritesKeys = {
  all: ["favorites"] as const,
  lists: () => [...favoritesKeys.all, "list"] as const,
  list: (filters?: any) => [...favoritesKeys.lists(), { filters }] as const,
  detail: (id: string) => [...favoritesKeys.all, "detail", id] as const,
  check: (actividadId: string) =>
    [...favoritesKeys.all, "check", actividadId] as const,
  count: () => [...favoritesKeys.all, "count"] as const,
};

/**
 * Hook to get user's favorites with pagination and filters
 */
export function useFavorites(params?: {
  page?: number;
  page_size?: number;
  tipo?: string;
  localidad?: string;
}) {
  return useQuery({
    queryKey: favoritesKeys.list(params),
    queryFn: () => favoritesApi.getUserFavorites(params),
  });
}

/**
 * Hook to check if an activity is favorited
 */
export function useIsFavorite(actividadId: string) {
  return useQuery({
    queryKey: favoritesKeys.check(actividadId),
    queryFn: () => favoritesApi.checkIsFavorite(actividadId),
    enabled: !!actividadId,
  });
}

/**
 * Hook to get favorite count
 */
export function useFavoriteCount() {
  return useQuery({
    queryKey: favoritesKeys.count(),
    queryFn: favoritesApi.getFavoriteCount,
  });
}

/**
 * Hook to add an activity to favorites
 * Includes optimistic updates for better UX
 */
export function useAddFavorite() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: favoritesApi.addFavorite,
    
    // Optimistic update
    onMutate: async (actividadId: string) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: favoritesKeys.check(actividadId) });
      
      // Snapshot previous value
      const previousCheck = queryClient.getQueryData(favoritesKeys.check(actividadId));
      
      // Optimistically update to the new value
      queryClient.setQueryData(favoritesKeys.check(actividadId), {
        is_favorite: true,
        favorito_id: "temp-id",
      });
      
      return { previousCheck };
    },
    
    onSuccess: (_data, actividadId) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: favoritesKeys.lists() });
      queryClient.invalidateQueries({ queryKey: favoritesKeys.check(actividadId) });
      queryClient.invalidateQueries({ queryKey: favoritesKeys.count() });
      queryClient.invalidateQueries({ queryKey: ["recommendations"] });
      
      toast({
        title: "✅ Agregado a favoritos",
        description: "La actividad se agregó a tus favoritos",
      });
    },
    
    onError: (_error, actividadId, context) => {
      // Revert optimistic update
      if (context?.previousCheck) {
        queryClient.setQueryData(favoritesKeys.check(actividadId), context.previousCheck);
      }
      
      toast({
        variant: "destructive",
        title: "Error",
        description: "No se pudo agregar a favoritos. Intenta de nuevo.",
      });
    },
  });
}

/**
 * Hook to remove an activity from favorites
 * Includes optimistic updates for better UX
 */
export function useRemoveFavorite() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: favoritesApi.removeFavorite,
    
    // Optimistic update
    onMutate: async (actividadId: string) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: favoritesKeys.check(actividadId) });
      
      // Snapshot previous value
      const previousCheck = queryClient.getQueryData(favoritesKeys.check(actividadId));
      
      // Optimistically update to the new value
      queryClient.setQueryData(favoritesKeys.check(actividadId), {
        is_favorite: false,
        favorito_id: null,
      });
      
      return { previousCheck };
    },
    
    onSuccess: (_data, actividadId) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: favoritesKeys.lists() });
      queryClient.invalidateQueries({ queryKey: favoritesKeys.check(actividadId) });
      queryClient.invalidateQueries({ queryKey: favoritesKeys.count() });
      queryClient.invalidateQueries({ queryKey: ["recommendations"] });
      
      toast({
        title: "Eliminado de favoritos",
        description: "La actividad se eliminó de tus favoritos",
      });
    },
    
    onError: (_error, actividadId, context) => {
      // Revert optimistic update
      if (context?.previousCheck) {
        queryClient.setQueryData(favoritesKeys.check(actividadId), context.previousCheck);
      }
      
      toast({
        variant: "destructive",
        title: "Error",
        description: "No se pudo eliminar de favoritos. Intenta de nuevo.",
      });
    },
  });
}
