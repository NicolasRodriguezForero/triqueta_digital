import { createFileRoute, Link } from "@tanstack/react-router";
import { useCurrentUser } from "../hooks/useAuth";
import { Button } from "../components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const { data: user, isLoading } = useCurrentUser();

  return (
    <section className="flex-1 w-full flex flex-col items-center justify-center">
      <div className="max-w-4xl text-center">
        <h1 className="text-5xl font-bold mb-4">
          Bienvenido a <span className="">Triqueta Digital</span>
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
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
          <Card>
            <CardHeader>
              <CardTitle>🎭 Cultural</CardTitle>
              <CardDescription>
                Teatro, museos, exposiciones y más
              </CardDescription>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>⚽ Deportiva</CardTitle>
              <CardDescription>
                Eventos deportivos y actividad física
              </CardDescription>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>🎉 Recreativa</CardTitle>
              <CardDescription>
                Festivales, conciertos y eventos comunitarios
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </div>
    </section>
  );
}
