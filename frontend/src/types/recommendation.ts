/**
 * Type definitions for recommendations.
 */

export interface RecommendationExplanation {
  reason: string;
  details: string;
}

export interface RecommendationResponse {
  actividad: any; // Will use Actividad type from activities.ts
  score: number;
  explanation: RecommendationExplanation;
  is_favorite: boolean;
}

export interface RecommendationList {
  items: RecommendationResponse[];
  total: number;
  user_profile_complete: boolean;
}

export interface RecommendationQuery {
  limit?: number;
  tipo?: string;
  localidad?: string;
  exclude_favorited?: boolean;
}
