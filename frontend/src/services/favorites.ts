/**
 * Favorites API service
 */
import api from "./api";
import type {
  FavoritoCreate,
  FavoritoList,
  Favorito,
  IsFavoriteResponse,
} from "../types/favorite";

/**
 * Add activity to favorites
 */
export const addFavorite = async (
  actividad_id: string
): Promise<Favorito> => {
  const data: FavoritoCreate = { actividad_id };
  const response = await api.post<Favorito>("/favoritos", data);
  return response.data;
};

/**
 * Remove activity from favorites
 */
export const removeFavorite = async (actividad_id: string): Promise<void> => {
  await api.delete(`/favoritos/${actividad_id}`);
};

/**
 * Get user's favorites with pagination and filters
 */
export const getUserFavorites = async (params?: {
  page?: number;
  page_size?: number;
  tipo?: string;
  localidad?: string;
}): Promise<FavoritoList> => {
  const response = await api.get<FavoritoList>("/favoritos", { params });
  return response.data;
};

/**
 * Check if activity is favorited
 */
export const checkIsFavorite = async (
  actividad_id: string
): Promise<IsFavoriteResponse> => {
  const response = await api.get<IsFavoriteResponse>(
    `/favoritos/check/${actividad_id}`
  );
  return response.data;
};

/**
 * Get total favorite count
 */
export const getFavoriteCount = async (): Promise<number> => {
  const response = await api.get<{ count: number }>("/favoritos/count");
  return response.data.count;
};
