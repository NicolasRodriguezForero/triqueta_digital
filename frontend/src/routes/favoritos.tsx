/**
 * Favoritos page - Lista de actividades favoritas del usuario
 */
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Loader2, Heart, Filter } from "lucide-react";
import { useFavorites } from "@/hooks/useFavorites";
import { ActivityCard } from "@/components/ActivityCard";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/favoritos" as any)({
  component: FavoritosPage,
});

function FavoritosPage() {
  const [tipo, setTipo] = useState<string | undefined>();
  const [localidad, setLocalidad] = useState<string | undefined>();
  const [page, setPage] = useState(1);

  const { data, isLoading, isError } = useFavorites({
    page,
    page_size: 12,
    tipo,
    localidad,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Error al cargar favoritos</p>
      </div>
    );
  }

  const hasFavorites = data && data.total > 0;

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Heart className="w-8 h-8 text-red-500 fill-current" />
          <h1 className="text-3xl font-bold">Mis Favoritos</h1>
        </div>
        <p className="text-gray-600">
          {data?.total || 0} actividades guardadas
        </p>
      </div>

      {/* Filters */}
      {hasFavorites && (
        <div className="mb-6 flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <span className="text-sm font-medium">Filtros:</span>
          </div>

          <Select value={tipo} onValueChange={setTipo}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Tipo de actividad" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="*">Todos los tipos</SelectItem>
              <SelectItem value="cultura">Cultura</SelectItem>
              <SelectItem value="deporte">Deporte</SelectItem>
              <SelectItem value="recreacion">Recreación</SelectItem>
            </SelectContent>
          </Select>

          <Select value={localidad} onValueChange={setLocalidad}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Localidad" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="*">Todas las localidades</SelectItem>
              <SelectItem value="Chapinero">Chapinero</SelectItem>
              <SelectItem value="Santa Fe">Santa Fe</SelectItem>
              <SelectItem value="La Candelaria">La Candelaria</SelectItem>
            </SelectContent>
          </Select>

          {(tipo || localidad) && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setTipo(undefined);
                setLocalidad(undefined);
              }}
            >
              Limpiar filtros
            </Button>
          )}
        </div>
      )}

      {/* Content */}
      {!hasFavorites ? (
        <div className="text-center py-16">
          <Heart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold mb-2">
            No tienes favoritos aún
          </h2>
          <p className="text-gray-600 mb-6">
            Explora actividades y guarda tus favoritas aquí
          </p>
          <Button onClick={() => (window.location.href = "/actividades")}>
            Explorar actividades
          </Button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data?.items.map((favorito) => (
              <ActivityCard
                key={favorito.id}
                activity={favorito.actividad as any}
              />
            ))}
          </div>

          {/* Pagination */}
          {data && data.total_pages > 1 && (
            <div className="flex justify-center gap-2 mt-8">
              <Button
                variant="outline"
                onClick={() => setPage(page - 1)}
                disabled={page === 1}
              >
                Anterior
              </Button>
              <span className="flex items-center px-4">
                Página {page} de {data.total_pages}
              </span>
              <Button
                variant="outline"
                onClick={() => setPage(page + 1)}
                disabled={page >= data.total_pages}
              >
                Siguiente
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
