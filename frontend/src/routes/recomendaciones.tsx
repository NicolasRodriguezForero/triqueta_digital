/**
 * Recomendaciones page - Actividades personalizadas para el usuario
 */
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Loader2, Sparkles, Lightbulb, Info } from "lucide-react";
import { useRecommendations } from "@/hooks/useRecommendations";
import { ActivityCard } from "@/components/ActivityCard";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";

export const Route = createFileRoute("/recomendaciones" as any)({
  component: RecomendacionesPage,
});

function RecomendacionesPage() {
  const [tipo, setTipo] = useState<string | undefined>();
  const [localidad, setLocalidad] = useState<string | undefined>();
  const [limit, setLimit] = useState(12);
  const [excludeFavorited, setExcludeFavorited] = useState(false);

  const { data, isLoading, isError, refetch } = useRecommendations({
    limit,
    tipo,
    localidad,
    exclude_favorited: excludeFavorited,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Error al cargar recomendaciones</p>
        <Button onClick={() => refetch()} className="mt-4">
          Reintentar
        </Button>
      </div>
    );
  }

  const hasRecommendations = data && data.total > 0;

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-8 h-8 text-purple-600" />
          <h1 className="text-3xl font-bold">Recomendaciones para ti</h1>
        </div>
        <p className="text-gray-600">
          Actividades personalizadas basadas en tus intereses
        </p>
      </div>

      {/* Profile Incomplete Alert */}
      {data && !data.user_profile_complete && (
        <Alert className="mb-6">
          <Info className="h-4 w-4" />
          <AlertDescription>
            <strong>Completa tu perfil</strong> para obtener recomendaciones más
            personalizadas. Agrega tus intereses, localidad preferida y nivel de
            actividad en la{" "}
            <a
              href="/perfil"
              className="underline font-medium hover:text-blue-600"
            >
              configuración de perfil
            </a>
            .
          </AlertDescription>
        </Alert>
      )}

      {/* Filters */}
      <div className="mb-6 flex flex-wrap gap-4">
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

        <Button
          variant={excludeFavorited ? "default" : "outline"}
          onClick={() => setExcludeFavorited(!excludeFavorited)}
        >
          {excludeFavorited ? "Mostrando no guardados" : "Excluir guardados"}
        </Button>

        {(tipo || localidad) && (
          <Button
            variant="outline"
            onClick={() => {
              setTipo(undefined);
              setLocalidad(undefined);
            }}
          >
            Limpiar filtros
          </Button>
        )}
      </div>

      {/* Content */}
      {!hasRecommendations ? (
        <div className="text-center py-16">
          <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold mb-2">
            No hay recomendaciones disponibles
          </h2>
          <p className="text-gray-600 mb-6">
            Prueba ajustando los filtros o explora todas las actividades
          </p>
          <Button onClick={() => (window.location.href = "/actividades")}>
            Ver todas las actividades
          </Button>
        </div>
      ) : (
        <>
          <div className="space-y-6">
            {data?.items.map((recommendation, index) => (
              <div
                key={`${recommendation.actividad.id}-${index}`}
                className="relative"
              >
                {/* Recommendation Card */}
                <div className="bg-white rounded-lg shadow-sm border p-4 mb-2">
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                    {/* Activity Card */}
                    <div className="lg:col-span-2">
                      <ActivityCard activity={recommendation.actividad as any} />
                    </div>

                    {/* Recommendation Info */}
                    <div className="flex flex-col justify-center gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <Sparkles className="w-5 h-5 text-purple-600" />
                          <span className="font-semibold">
                            Puntuación: {recommendation.score.toFixed(0)}/100
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-purple-600 h-2 rounded-full transition-all"
                            style={{ width: `${recommendation.score}%` }}
                          />
                        </div>
                      </div>

                      <div className="bg-purple-50 rounded-lg p-3">
                        <div className="flex items-start gap-2">
                          <Lightbulb className="w-4 h-4 text-purple-600 mt-0.5 flex-shrink-0" />
                          <div>
                            <p className="text-sm font-medium text-purple-900 mb-1">
                              ¿Por qué se recomienda?
                            </p>
                            <Badge className="bg-purple-100 text-purple-800 mb-2">
                              {recommendation.explanation.reason === "tags"
                                ? "Coincidencia de intereses"
                                : recommendation.explanation.reason ===
                                  "location"
                                ? "En tu zona"
                                : "Popular"}
                            </Badge>
                            <p className="text-sm text-purple-800">
                              {recommendation.explanation.details}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Load More */}
          {data && data.total > limit && (
            <div className="text-center mt-8">
              <Button onClick={() => setLimit(limit + 12)}>
                Cargar más recomendaciones
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
