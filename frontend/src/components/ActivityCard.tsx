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
        return "bg-purple-100 text-purple-800 hover:bg-purple-200";
      case "deporte":
        return "bg-green-100 text-green-800 hover:bg-green-200";
      case "recreacion":
        return "bg-blue-100 text-blue-800 hover:bg-blue-200";
      default:
        return "bg-gray-100 text-gray-800 hover:bg-gray-200";
    }
  };

  return (
    <Link
      to="/actividades/$id"
      params={{ id: activity.id }}
      className="block group"
    >
      <Card className="h-full transition-all duration-200 hover:shadow-lg hover:-translate-y-1">
        {/* Image */}
        {activity.imagen_url && (
          <div className="relative h-48 overflow-hidden rounded-t-lg -mt-6">
            <img
              src={activity.imagen_url}
              alt={activity.titulo}
              className="w-full h-full object-cover transition-transform duration-200 group-hover:scale-105"
            />
            {activity.es_gratis && (
              <Badge className="absolute top-2 right-2 bg-green-600 text-white">
                Gratis
              </Badge>
            )}
          </div>
        )}

        <CardHeader>
          <div className="flex items-start justify-between gap-2 mb-2">
            <Badge className={getTipoColor(activity.tipo)}>
              {activity.tipo.charAt(0).toUpperCase() + activity.tipo.slice(1)}
            </Badge>
            {!activity.es_gratis && (
              <span className="text-sm font-semibold text-green-600">
                ${activity.precio.toLocaleString("es-CO")}
              </span>
            )}
          </div>
          <CardTitle className="line-clamp-2 group-hover:text-blue-600 transition-colors">
            {activity.titulo}
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-3">
          {/* Description */}
          <p className="text-sm text-gray-600 line-clamp-2">
            {activity.descripcion}
          </p>

          {/* Date */}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Calendar className="w-4 h-4 flex-shrink-0" />
            <span className="truncate">
              {formatDate(activity.fecha_inicio)}
              {activity.fecha_fin && ` - ${formatDate(activity.fecha_fin)}`}
            </span>
          </div>

          {/* Location */}
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <MapPin className="w-4 h-4 flex-shrink-0" />
            <span className="truncate">{activity.localidad}</span>
          </div>

          {/* Tags */}
          {activity.etiquetas.length > 0 && (
            <div className="flex items-start gap-2">
              <Tag className="w-4 h-4 flex-shrink-0 mt-0.5 text-gray-400" />
              <div className="flex flex-wrap gap-1">
                {activity.etiquetas.slice(0, 3).map((tag) => (
                  <Badge key={tag} variant="secondary" className="text-xs">
                    {tag}
                  </Badge>
                ))}
                {activity.etiquetas.length > 3 && (
                  <Badge variant="secondary" className="text-xs">
                    +{activity.etiquetas.length - 3}
                  </Badge>
                )}
              </div>
            </div>
          )}
        </CardContent>

        <CardFooter className="text-xs text-gray-500 pt-4 border-t">
          <div className="flex items-center justify-between w-full">
            <span className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              {activity.popularidad_vistas || 0} vistas
            </span>
            <span className="flex items-center gap-1">
              <Star className="w-3 h-3" />
              {activity.popularidad_favoritos || 0} favoritos
            </span>
          </div>
        </CardFooter>
      </Card>
    </Link>
  );
}
