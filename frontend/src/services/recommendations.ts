/**
 * Recommendations API service
 */
import api from "./api";
import type {
  RecommendationList,
  RecommendationQuery,
} from "../types/recommendation";

/**
 * Get personalized recommendations for the current user
 */
export const getRecommendations = async (
  params?: RecommendationQuery
): Promise<RecommendationList> => {
  const response = await api.get<RecommendationList>("/recomendaciones", {
    params,
  });
  return response.data;
};
