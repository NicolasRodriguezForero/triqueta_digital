/**
 * Activity detail page (RF-010)
 */
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  Loader2,
  AlertCircle,
  Calendar,
  MapPin,
  Tag,
  DollarSign,
  ExternalLink,
  Phone,
  ArrowLeft,
} from "lucide-react";
import { useActivity } from "../hooks/useActivities";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { FavoriteButton } from "@/components/FavoriteButton";

export const Route = createFileRoute("/actividades/$id")({
  component: ActividadDetailPage,
});

function ActividadDetailPage() {
  const { id } = Route.useParams();
  const navigate = useNavigate();
  const { data: activity, isLoading, isError, error } = useActivity(id);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("es-CO", {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getTipoColor = (tipo: string) => {
    switch (tipo) {
      case "cultura":
        return "bg-purple-100 text-purple-800";
      case "deporte":
        return "bg-green-100 text-green-800";
      case "recreacion":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getNivelColor = (nivel: string) => {
    switch (nivel) {
      case "bajo":
        return "bg-green-100 text-green-800";
      case "medio":
        return "bg-yellow-100 text-yellow-800";
      case "alto":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center items-center py-12">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      </div>
    );
  }

  if (isError || !activity) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Alert variant="destructive" className="mb-8">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error al cargar actividad</AlertTitle>
          <AlertDescription>
            {error instanceof Error
              ? error.message
              : "No se pudo cargar la información de la actividad."}
          </AlertDescription>
        </Alert>
        <Button
          onClick={() => navigate({ to: "/actividades" })}
          variant="outline"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a actividades
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Back Button */}
      <Button
        onClick={() => navigate({ to: "/actividades" })}
        variant="ghost"
        className="mb-6"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Volver a actividades
      </Button>

      {/* Hero Image */}
      {activity.imagen_url && (
        <div className="relative h-96 w-full overflow-hidden rounded-lg mb-8">
          <img
            src={activity.imagen_url}
            alt={activity.titulo}
            className="w-full h-full object-cover"
          />
          {activity.es_gratis && (
            <Badge className="absolute top-4 right-4 bg-green-600 text-white text-base px-4 py-2">
              Gratis
            </Badge>
          )}
        </div>
      )}

      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-2 mb-4">
          <Badge className={getTipoColor(activity.tipo)}>
            {activity.tipo.charAt(0).toUpperCase() + activity.tipo.slice(1)}
          </Badge>
          {activity.nivel_actividad && (
            <Badge className={getNivelColor(activity.nivel_actividad)}>
              Nivel {activity.nivel_actividad}
            </Badge>
          )}
          {!activity.es_gratis && (
            <Badge
              variant="outline"
              className="text-green-600 border-green-600"
            >
              <DollarSign className="w-4 h-4 mr-1" />$
              {activity.precio.toLocaleString("es-CO")}
            </Badge>
          )}
        </div>

        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          {activity.titulo}
        </h1>

        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-6 text-gray-600">
            <span>
              👁️ {Math.round((activity.popularidad_vistas || 0) * 10)} vistas
            </span>
            <span>⭐ {activity.popularidad_favoritos} favoritos</span>
          </div>

          <FavoriteButton
            actividadId={activity.id}
            variant="default"
            showLabel={true}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          <Card>
            <CardHeader>
              <CardTitle>Descripción</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                {activity.descripcion}
              </div>
            </CardContent>
          </Card>

          {/* Tags */}
          {activity.etiquetas.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Tag className="w-5 h-5" />
                  Etiquetas
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {activity.etiquetas.map((tag) => (
                    <Badge key={tag} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Date and Time */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                Fecha y hora
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-gray-600 mb-1">Inicio</p>
                <p className="font-medium">
                  {formatDate(activity.fecha_inicio)}
                </p>
              </div>
              {activity.fecha_fin && (
                <div>
                  <p className="text-sm text-gray-600 mb-1">Fin</p>
                  <p className="font-medium">
                    {formatDate(activity.fecha_fin)}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Location */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MapPin className="w-5 h-5" />
                Ubicación
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm text-gray-600 mb-1">Localidad</p>
                <p className="font-medium">{activity.localidad}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Dirección</p>
                <p className="font-medium">{activity.ubicacion_direccion}</p>
              </div>
              {/* Future: Add map with activity.ubicacion_lat, activity.ubicacion_lng */}
            </CardContent>
          </Card>

          {/* Contact */}
          {(activity.contacto || activity.enlace_externo) && (
            <Card>
              <CardHeader>
                <CardTitle>Contacto</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {activity.contacto && (
                  <div className="flex items-center gap-2 text-sm">
                    <Phone className="w-4 h-4 text-gray-600" />
                    <span>{activity.contacto}</span>
                  </div>
                )}
                {activity.enlace_externo && (
                  <Button asChild variant="outline" className="w-full">
                    <a
                      href={activity.enlace_externo}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <ExternalLink className="w-4 h-4 mr-2" />
                      Más información
                    </a>
                  </Button>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
