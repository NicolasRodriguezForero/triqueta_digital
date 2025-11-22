/**
 * Activities list page with search, filters and pagination (RF-007, RF-008)
 */
import { useState } from "react";
import { createFileRoute, Outlet, useLocation } from "@tanstack/react-router";
import { Loader2, AlertCircle } from "lucide-react";
import { ActivityCard } from "../components/ActivityCard";
import { SearchBar } from "../components/SearchBar";
import {
  ActivityFilters,
  type FilterValues,
} from "../components/ActivityFilters";
import { useActivities } from "../hooks/useActivities";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

export const Route = createFileRoute("/actividades")({
  component: ActividadesLayout,
});

function ActividadesLayout() {
  const location = useLocation();

  // If we're on a child route (like /actividades/$id), render only the child
  if (location.pathname !== "/actividades") {
    return <Outlet />;
  }

  // Otherwise render the main actividades page
  return <ActividadesPage />;
}

function ActividadesPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<FilterValues>({});
  const [page, setPage] = useState(0);
  const limit = 12;

  // Fetch activities with current filters
  const { data, isLoading, isError, error } = useActivities({
    q: searchQuery || undefined,
    ...filters,
    skip: page * limit,
    limit,
  });

  const handleClearFilters = () => {
    setFilters({});
    setSearchQuery("");
    setPage(0);
  };

  const handleFilterChange = (newFilters: FilterValues) => {
    setFilters(newFilters);
    setPage(0); // Reset to first page when filters change
  };

  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
    setPage(0); // Reset to first page when search changes
  };

  const hasActiveFilters = Object.keys(filters).length > 0 || searchQuery;

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-10 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-accent/5 to-primary/5 rounded-2xl blur-3xl -z-10"></div>
        <div className="relative">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center shadow-lg">
              <span className="text-2xl">🎯</span>
            </div>
            <div>
              <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent mb-2">
                Explora Actividades
              </h1>
              <p className="text-lg text-muted-foreground">
                Descubre experiencias increíbles en Bogotá
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <SearchBar
              value={searchQuery}
              onChange={handleSearchChange}
              placeholder="Buscar por título, descripción o etiquetas..."
            />
          </div>
          <ActivityFilters
            filters={filters}
            onChange={handleFilterChange}
            onClear={handleClearFilters}
          />
        </div>

        {/* Active filters summary */}
        {hasActiveFilters && data && (
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Se encontraron{" "}
            <span className="font-semibold">{data.pagination.total}</span>{" "}
            actividades
          </p>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      )}

      {/* Error State */}
      {isError && (
        <Alert variant="destructive" className="mb-8">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error al cargar actividades</AlertTitle>
          <AlertDescription>
            {error instanceof Error
              ? error.message
              : "Ocurrió un error al cargar las actividades. Por favor, intenta de nuevo."}
          </AlertDescription>
        </Alert>
      )}

      {/* Activities Grid */}
      {data && !isLoading && (
        <>
          {data.data.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">
                No se encontraron actividades con los filtros seleccionados.
              </p>
              {hasActiveFilters && (
                <Button onClick={handleClearFilters} variant="outline">
                  Limpiar filtros
                </Button>
              )}
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
                {data.data.map((activity) => (
                  <ActivityCard key={activity.id} activity={activity} />
                ))}
              </div>

              {/* Pagination */}
              {data.pagination.total > limit && (
                <div className="flex justify-center items-center gap-4">
                  <Button
                    onClick={() => setPage(page - 1)}
                    disabled={page === 0}
                    variant="outline"
                  >
                    Anterior
                  </Button>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Página {page + 1} de{" "}
                    {Math.ceil(data.pagination.total / limit)}
                  </span>
                  <Button
                    onClick={() => setPage(page + 1)}
                    disabled={!data.pagination.has_more}
                    variant="outline"
                  >
                    Siguiente
                  </Button>
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  );
}
