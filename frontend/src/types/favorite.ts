/**
 * Type definitions for favorites.
 */

export interface Favorito {
  id: string;
  usuario_id: number;
  actividad_id: string;
  fecha_guardado: string;
}

export interface FavoritoCreate {
  actividad_id: string;
}

export interface FavoritoWithActivity extends Favorito {
  actividad: any; // Will use Actividad type from activities.ts
}

export interface FavoritoList {
  items: FavoritoWithActivity[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface IsFavoriteResponse {
  is_favorite: boolean;
  favorito_id: string | null;
}
