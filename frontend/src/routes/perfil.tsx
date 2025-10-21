import { createFileRoute, Navigate } from "@tanstack/react-router";
import { useProfile, useUpdateProfile } from "../hooks/useProfile";
import { useIsAuthenticated } from "../hooks/useAuth";
import { useState } from "react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";

export const Route = createFileRoute("/perfil")({
  component: PerfilPage,
});

function PerfilPage() {
  const isAuthenticated = useIsAuthenticated();
  const { data: user, isLoading } = useProfile();
  const updateProfile = useUpdateProfile();
  
  const [nombreCompleto, setNombreCompleto] = useState("");
  const [telefono, setTelefono] = useState("");
  const [biografia, setBiografia] = useState("");
  const [localidadPreferida, setLocalidadPreferida] = useState("");
  const [disponibilidad, setDisponibilidad] = useState("");
  const [nivelActividad, setNivelActividad] = useState("");
  const [etiquetasInteres, setEtiquetasInteres] = useState("");
  
  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  // Initialize form when data loads
  if (user && !nombreCompleto && user.perfil) {
    setNombreCompleto(user.perfil.nombre_completo || "");
    setTelefono(user.perfil.telefono || "");
    setBiografia(user.perfil.biografia || "");
    setLocalidadPreferida(user.perfil.localidad_preferida || "");
    setDisponibilidad(user.perfil.disponibilidad_horaria || "");
    setNivelActividad(user.perfil.nivel_actividad || "");
    setEtiquetasInteres(user.perfil.etiquetas_interes.join(", "));
  }
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    updateProfile.mutate({
      nombre_completo: nombreCompleto,
      telefono: telefono,
      biografia: biografia,
      localidad_preferida: localidadPreferida,
      disponibilidad_horaria: disponibilidad,
      nivel_actividad: nivelActividad,
      etiquetas_interes: etiquetasInteres.split(",").map(tag => tag.trim()).filter(Boolean),
    });
  };
  
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="h-8 w-48 bg-gray-200 animate-pulse rounded mb-4" />
          <div className="h-64 bg-gray-200 animate-pulse rounded" />
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Mi Perfil</h1>
        
        <Card>
          <CardHeader>
            <CardTitle>Información Personal</CardTitle>
            <CardDescription>
              Actualiza tu información y preferencias
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={user?.email || ""}
                  disabled
                  className="bg-gray-100"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="nombreCompleto">Nombre Completo</Label>
                <Input
                  id="nombreCompleto"
                  type="text"
                  value={nombreCompleto}
                  onChange={(e) => setNombreCompleto(e.target.value)}
                  placeholder="Tu nombre completo"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="telefono">Teléfono</Label>
                <Input
                  id="telefono"
                  type="tel"
                  value={telefono}
                  onChange={(e) => setTelefono(e.target.value)}
                  placeholder="3001234567"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="biografia">Biografía</Label>
                <textarea
                  id="biografia"
                  value={biografia}
                  onChange={(e) => setBiografia(e.target.value)}
                  placeholder="Cuéntanos sobre ti..."
                  className="w-full min-h-[100px] px-3 py-2 border rounded-md"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="localidadPreferida">Localidad Preferida</Label>
                <select
                  id="localidadPreferida"
                  value={localidadPreferida}
                  onChange={(e) => setLocalidadPreferida(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="">Selecciona una localidad</option>
                  <option value="Chapinero">Chapinero</option>
                  <option value="Santa Fe">Santa Fe</option>
                  <option value="La Candelaria">La Candelaria</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="disponibilidad">Disponibilidad Horaria</Label>
                <select
                  id="disponibilidad"
                  value={disponibilidad}
                  onChange={(e) => setDisponibilidad(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="">Selecciona tu disponibilidad</option>
                  <option value="mañana">Mañana</option>
                  <option value="tarde">Tarde</option>
                  <option value="noche">Noche</option>
                  <option value="fin_de_semana">Fin de semana</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="nivelActividad">Nivel de Actividad</Label>
                <select
                  id="nivelActividad"
                  value={nivelActividad}
                  onChange={(e) => setNivelActividad(e.target.value)}
                  className="w-full px-3 py-2 border rounded-md"
                >
                  <option value="">Selecciona tu nivel</option>
                  <option value="bajo">Bajo</option>
                  <option value="medio">Medio</option>
                  <option value="alto">Alto</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="etiquetasInteres">Intereses</Label>
                <Input
                  id="etiquetasInteres"
                  type="text"
                  value={etiquetasInteres}
                  onChange={(e) => setEtiquetasInteres(e.target.value)}
                  placeholder="arte, música, deportes (separados por coma)"
                />
                <p className="text-sm text-gray-500">
                  Separa tus intereses con comas
                </p>
              </div>
              
              {updateProfile.isError && (
                <p className="text-sm text-red-600">
                  Error al actualizar perfil
                </p>
              )}
              
              {updateProfile.isSuccess && (
                <p className="text-sm text-green-600">
                  ¡Perfil actualizado exitosamente!
                </p>
              )}
              
              <Button
                type="submit"
                className="w-full"
                disabled={updateProfile.isPending}
              >
                {updateProfile.isPending ? "Guardando..." : "Guardar Cambios"}
              </Button>
            </CardContent>
          </form>
        </Card>
      </div>
    </div>
  );
}
