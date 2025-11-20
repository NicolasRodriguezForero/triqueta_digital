/**
 * React Query hooks for recommendations functionality
 */
import { useQuery } from "@tanstack/react-query";
import * as recommendationsApi from "../services/recommendations";
import type { RecommendationQuery } from "../types/recommendation";

/**
 * Query key factory for recommendations
 */
export const recommendationsKeys = {
  all: ["recommendations"] as const,
  lists: () => [...recommendationsKeys.all, "list"] as const,
  list: (params?: RecommendationQuery) =>
    [...recommendationsKeys.lists(), { params }] as const,
};

/**
 * Hook to get personalized recommendations
 */
export function useRecommendations(params?: RecommendationQuery) {
  return useQuery({
    queryKey: recommendationsKeys.list(params),
    queryFn: () => recommendationsApi.getRecommendations(params),
    staleTime: 1000 * 60 * 5, // Consider data fresh for 5 minutes
  });
}
