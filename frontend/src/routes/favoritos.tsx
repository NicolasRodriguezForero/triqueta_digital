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
      <div className="mb-10 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-red-500/5 via-pink-500/5 to-red-500/5 rounded-2xl blur-3xl -z-10"></div>
        <div className="relative">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-red-500 to-pink-500 flex items-center justify-center shadow-lg">
              <Heart className="w-7 h-7 text-white fill-white" />
            </div>
            <div>
              <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent mb-2">
                Mis Favoritos
              </h1>
              <p className="text-lg text-muted-foreground">
                {data?.total || 0} {data?.total === 1 ? 'actividad guardada' : 'actividades guardadas'}
              </p>
            </div>
          </div>
        </div>
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
        <div className="text-center py-20">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-red-500/10 to-pink-500/10 mb-6">
            <Heart className="w-10 h-10 text-red-400" />
          </div>
          <h2 className="text-2xl font-semibold mb-3">
            Tu lista de favoritos está vacía
          </h2>
          <p className="text-muted-foreground mb-8 max-w-md mx-auto">
            Explora actividades increíbles y guarda tus favoritas para encontrarlas fácilmente después
          </p>
          <Button 
            onClick={() => (window.location.href = "/actividades")} 
            size="lg"
            className="gap-2"
          >
            <Heart className="w-4 h-4" />
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
