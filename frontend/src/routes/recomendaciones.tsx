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
      <div className="mb-10 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 via-primary/5 to-purple-500/5 rounded-2xl blur-3xl -z-10"></div>
        <div className="relative">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-500 to-primary flex items-center justify-center shadow-lg">
              <Sparkles className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent mb-2">
                Recomendaciones para ti
              </h1>
              <p className="text-lg text-muted-foreground">
                Actividades personalizadas basadas en tus intereses y preferencias
              </p>
            </div>
          </div>
        </div>
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
        <div className="text-center py-20">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-muted mb-6">
            <Lightbulb className="w-10 h-10 text-muted-foreground" />
          </div>
          <h2 className="text-2xl font-semibold mb-3">
            No hay recomendaciones disponibles
          </h2>
          <p className="text-muted-foreground mb-8 max-w-md mx-auto">
            Prueba ajustando los filtros o completa tu perfil para obtener recomendaciones más personalizadas
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button onClick={() => (window.location.href = "/actividades")} variant="outline">
              Ver todas las actividades
            </Button>
            <Button onClick={() => (window.location.href = "/perfil")}>
              Completar mi perfil
            </Button>
          </div>
        </div>
      ) : (
        <>
          <div className="space-y-6">
            {data?.items.map((recommendation, index) => (
              <div
                key={`${recommendation.actividad.id}-${index}`}
                className="relative group"
              >
                {/* Recommendation Card with gradient border */}
                <div className="relative bg-card rounded-xl shadow-lg border-2 border-border hover:border-primary/30 transition-all duration-300 overflow-hidden">
                  {/* Gradient accent bar */}
                  <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 via-primary to-purple-500"></div>
                  
                  <div className="p-6">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      {/* Activity Card */}
                      <div className="lg:col-span-2">
                        <ActivityCard activity={recommendation.actividad as any} />
                      </div>

                      {/* Recommendation Info */}
                      <div className="flex flex-col justify-between gap-6">
                        {/* Score Section */}
                        <div className="space-y-3">
                          <div className="flex items-center gap-2">
                            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-primary flex items-center justify-center">
                              <Sparkles className="w-5 h-5 text-white" />
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground uppercase tracking-wide">Puntuación</p>
                              <p className="text-2xl font-bold text-foreground">
                                {recommendation.score.toFixed(0)}<span className="text-lg text-muted-foreground">/100</span>
                              </p>
                            </div>
                          </div>
                          <div className="space-y-2">
                            <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
                              <div
                                className="h-full rounded-full bg-gradient-to-r from-purple-500 to-primary transition-all duration-500 shadow-sm"
                                style={{ width: `${recommendation.score}%` }}
                              />
                            </div>
                            <p className="text-xs text-muted-foreground">
                              Basado en tus preferencias e intereses
                            </p>
                          </div>
                        </div>

                        {/* Explanation Section */}
                        <div className="bg-gradient-to-br from-purple-50 to-primary/5 dark:from-purple-950/30 dark:to-primary/5 rounded-xl p-4 border border-purple-200/50 dark:border-purple-800/50">
                          <div className="flex items-start gap-3">
                            <div className="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                              <Lightbulb className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                            </div>
                            <div className="flex-1 space-y-2">
                              <p className="text-sm font-semibold text-foreground">
                                ¿Por qué se recomienda?
                              </p>
                              <Badge className="bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-300 border-purple-200 dark:border-purple-800">
                                {recommendation.explanation.reason === "tags"
                                  ? "✨ Coincidencia de intereses"
                                  : recommendation.explanation.reason === "location"
                                  ? "📍 En tu zona"
                                  : "🔥 Popular"}
                              </Badge>
                              <p className="text-sm text-muted-foreground leading-relaxed">
                                {recommendation.explanation.details}
                              </p>
                            </div>
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
            <div className="text-center mt-10">
              <Button 
                onClick={() => setLimit(limit + 12)} 
                size="lg"
                className="gap-2"
              >
                <Sparkles className="w-4 h-4" />
                Cargar más recomendaciones
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
