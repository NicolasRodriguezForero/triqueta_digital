import { createFileRoute, Link } from "@tanstack/react-router";
import { useCurrentUser } from "../hooks/useAuth";
import { Button } from "../components/ui/button";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const { data: user, isLoading } = useCurrentUser();

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4">
          Bienvenido a <span className="text-blue-600">Triqueta Digital</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Conectando actividades culturales, recreativas y deportivas en Bogotá
        </p>

        {isLoading ? (
          <div className="h-12 w-48 bg-gray-200 animate-pulse rounded mx-auto" />
        ) : user ? (
          <div className="space-y-6">
            <p className="text-lg">
              ¡Hola, {user.perfil?.nombre_completo || user.email}!
            </p>
            <div className="flex justify-center gap-4">
              <Link to="/perfil">
                <Button size="lg">Ver mi Perfil</Button>
              </Link>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <p className="text-lg">
              Descubre actividades en Chapinero, Santa Fe y La Candelaria
            </p>
            <div className="flex justify-center gap-4">
              <Link to="/register">
                <Button size="lg">Crear Cuenta</Button>
              </Link>
              <Link to="/login">
                <Button size="lg" variant="outline">
                  Iniciar Sesión
                </Button>
              </Link>
            </div>
          </div>
        )}

        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="p-6 bg-white rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold mb-2">🎭 Cultural</h3>
            <p className="text-gray-600">
              Teatro, museos, exposiciones y más
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold mb-2">⚽ Deportiva</h3>
            <p className="text-gray-600">
              Eventos deportivos y actividad física
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg shadow-sm border">
            <h3 className="text-xl font-semibold mb-2">🎉 Recreativa</h3>
            <p className="text-gray-600">
              Festivales, conciertos y eventos comunitarios
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
