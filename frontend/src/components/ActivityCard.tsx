/**
 * ActivityCard component to display activity summary in a card format
 */
import { Link } from "@tanstack/react-router";
import { Calendar, Eye, MapPin, Star, Tag } from "lucide-react";
import type { Actividad } from "../services/activities";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FavoriteButton } from "./FavoriteButton";

interface ActivityCardProps {
  activity: Actividad;
}

export function ActivityCard({ activity }: ActivityCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("es-CO", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const getTipoColor = (tipo: string) => {
    switch (tipo) {
      case "cultura":
        return "bg-purple-100 dark:bg-purple-950/50 text-purple-800 dark:text-purple-300 border-purple-200 dark:border-purple-800";
      case "deporte":
        return "bg-green-100 dark:bg-green-950/50 text-green-800 dark:text-green-300 border-green-200 dark:border-green-800";
      case "recreacion":
        return "bg-blue-100 dark:bg-blue-950/50 text-blue-800 dark:text-blue-300 border-blue-200 dark:border-blue-800";
      default:
        return "bg-muted text-muted-foreground border-border";
    }
  };

  return (
    <Link
      to="/actividades/$id"
      params={{ id: activity.id }}
      className="block group"
    >
      <Card className="h-full transition-all duration-300 hover:shadow-xl hover:-translate-y-2 border-2 hover:border-primary/30 overflow-hidden relative">
        {/* Gradient overlay on hover */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/0 via-primary/0 to-primary/0 group-hover:from-primary/5 group-hover:via-primary/0 group-hover:to-accent/5 transition-all duration-300 pointer-events-none z-0"></div>
        
        <div className="relative z-10">
          {/* Image */}
          {activity.imagen_url ? (
            <div className="relative h-52 overflow-hidden -mt-6 -mx-6 mb-4">
              <img
                src={activity.imagen_url}
                alt={activity.titulo}
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-background/20 to-transparent"></div>
              {activity.es_gratis && (
                <Badge className="absolute top-3 right-3 bg-green-600 text-white shadow-lg border-2 border-white/20">
                  ✨ Gratis
                </Badge>
              )}
              <div className="absolute top-3 left-3">
                <Badge className={`${getTipoColor(activity.tipo)} shadow-md border-2 border-white/20`}>
                  {activity.tipo.charAt(0).toUpperCase() + activity.tipo.slice(1)}
                </Badge>
              </div>
            </div>
          ) : (
            <div className="relative h-32 overflow-hidden -mt-6 -mx-6 mb-4 bg-gradient-to-br from-primary/20 via-accent/20 to-primary/10 flex items-center justify-center">
              <div className="text-4xl">
                {activity.tipo === "cultura" ? "🎭" : activity.tipo === "deporte" ? "⚽" : "🎉"}
              </div>
              {activity.es_gratis && (
                <Badge className="absolute top-3 right-3 bg-green-600 text-white shadow-lg">
                  ✨ Gratis
                </Badge>
              )}
              <div className="absolute top-3 left-3">
                <Badge className={`${getTipoColor(activity.tipo)} shadow-md`}>
                  {activity.tipo.charAt(0).toUpperCase() + activity.tipo.slice(1)}
                </Badge>
              </div>
            </div>
          )}

          <CardHeader className="relative pb-3">
            <div className="absolute top-0 right-0 z-10">
              <FavoriteButton actividadId={activity.id} />
            </div>
            <div className="flex items-start justify-between gap-2 mb-3 pr-10">
              {!activity.es_gratis && (
                <div className="flex items-center gap-1 px-2 py-1 rounded-md bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-900">
                  <span className="text-sm font-bold text-green-700 dark:text-green-400">
                    ${activity.precio.toLocaleString("es-CO")}
                  </span>
                </div>
              )}
            </div>
            <CardTitle className="line-clamp-2 group-hover:text-primary transition-colors text-lg leading-tight">
              {activity.titulo}
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-3 pb-4">
            {/* Description */}
            <p className="text-sm text-muted-foreground line-clamp-2 leading-relaxed">
              {activity.descripcion}
            </p>

            {/* Date */}
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Calendar className="w-4 h-4 flex-shrink-0 text-primary/70" />
              <span className="truncate font-medium">
                {formatDate(activity.fecha_inicio)}
                {activity.fecha_fin && ` - ${formatDate(activity.fecha_fin)}`}
              </span>
            </div>

            {/* Location */}
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <MapPin className="w-4 h-4 flex-shrink-0 text-primary/70" />
              <span className="truncate font-medium">{activity.localidad}</span>
            </div>

            {/* Tags */}
            {activity.etiquetas.length > 0 && (
              <div className="flex items-start gap-2 pt-1">
                <Tag className="w-4 h-4 flex-shrink-0 mt-0.5 text-muted-foreground/50" />
                <div className="flex flex-wrap gap-1.5">
                  {activity.etiquetas.slice(0, 3).map((tag) => (
                    <Badge key={tag} variant="secondary" className="text-xs font-medium">
                      {tag}
                    </Badge>
                  ))}
                  {activity.etiquetas.length > 3 && (
                    <Badge variant="secondary" className="text-xs font-medium">
                      +{activity.etiquetas.length - 3}
                    </Badge>
                  )}
                </div>
              </div>
            )}
          </CardContent>

          <CardFooter className="text-xs text-muted-foreground pt-4 border-t bg-muted/30">
            <div className="flex items-center justify-between w-full">
              <span className="flex items-center gap-1.5 font-medium">
                <Eye className="w-3.5 h-3.5 text-primary/60" />
                {activity.popularidad_vistas || 0} vistas
              </span>
              <span className="flex items-center gap-1.5 font-medium">
                <Star className="w-3.5 h-3.5 text-primary/60 fill-primary/20" />
                {activity.popularidad_favoritos || 0} favoritos
              </span>
            </div>
          </CardFooter>
        </div>
      </Card>
    </Link>
  );
}
