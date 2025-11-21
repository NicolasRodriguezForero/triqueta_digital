import { createFileRoute, Link } from "@tanstack/react-router";
import { useCurrentUser } from "../hooks/useAuth";
import { Button } from "../components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Sparkles, MapPin, Heart, Zap, ArrowRight } from "lucide-react";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const { data: user, isLoading } = useCurrentUser();

  return (
    <section className="flex-1 w-full flex flex-col">
      {/* Hero Section with Gradient */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary/10 via-background to-accent/10 py-20 md:py-32">
        {/* Decorative background elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/5 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent/5 rounded-full blur-3xl"></div>
        </div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary mb-6 animate-fade-in">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm font-medium">Descubre tu próxima aventura</span>
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-foreground via-foreground/90 to-foreground/70 bg-clip-text text-transparent animate-fade-in-up">
              Bienvenido a{" "}
              <span className="bg-gradient-to-r from-primary to-accent-foreground bg-clip-text text-transparent">
                Triqueta Digital
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-muted-foreground mb-4 max-w-2xl mx-auto animate-fade-in-up animation-delay-200">
              Tu puerta de entrada al mundo cultural, deportivo y recreativo de{" "}
              <span className="font-semibold text-foreground">Bogotá</span>
            </p>
            
            <p className="text-lg text-muted-foreground/80 mb-12 max-w-xl mx-auto animate-fade-in-up animation-delay-400">
              Conectamos comunidades en Chapinero, Santa Fe y La Candelaria a través de experiencias únicas
            </p>

            {/* CTA Buttons */}
            {isLoading ? (
              <div className="h-12 w-48 bg-muted animate-pulse rounded-lg mx-auto" />
            ) : user ? (
              <div className="space-y-6 animate-fade-in-up animation-delay-600">
                <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-card border shadow-sm mb-4">
                  <Heart className="w-5 h-5 text-primary" />
                  <p className="text-lg font-medium">
                    ¡Hola, {user.perfil?.nombre_completo || user.email.split("@")[0]}! 👋
                  </p>
                </div>
                <div className="flex flex-col sm:flex-row justify-center gap-4">
                  <Link to="/actividades">
                    <Button size="lg" className="group gap-2">
                      Explorar Actividades
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </Link>
                  <Link to="/recomendaciones">
                    <Button size="lg" variant="outline" className="group gap-2">
                      <Sparkles className="w-4 h-4" />
                      Ver Recomendaciones
                    </Button>
                  </Link>
                </div>
              </div>
            ) : (
              <div className="space-y-6 animate-fade-in-up animation-delay-600">
                <div className="flex flex-col sm:flex-row justify-center gap-4">
                  <Link to="/register">
                    <Button size="lg" className="group gap-2 shadow-lg hover:shadow-xl transition-all">
                      Comenzar Ahora
                      <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </Link>
                  <Link to="/login">
                    <Button size="lg" variant="outline" className="group gap-2">
                      Iniciar Sesión
                    </Button>
                  </Link>
                </div>
                <p className="text-sm text-muted-foreground">
                  ✨ Únete a miles de personas descubriendo actividades increíbles
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16 md:py-24">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Todo lo que necesitas en un solo lugar
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Explora, guarda y descubre actividades que se adaptan a tus intereses
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 md:gap-8">
            <Card className="group border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <CardHeader className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-500/10 to-purple-600/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <span className="text-3xl">🎭</span>
                </div>
                <CardTitle className="text-2xl mb-2">Cultural</CardTitle>
                <CardDescription className="text-base">
                  Sumérgete en el arte, teatro, museos y exposiciones que enriquecen el alma
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="group border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <CardHeader className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-green-500/10 to-green-600/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <span className="text-3xl">⚽</span>
                </div>
                <CardTitle className="text-2xl mb-2">Deportiva</CardTitle>
                <CardDescription className="text-base">
                  Mantente activo con eventos deportivos y actividades físicas para todos los niveles
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="group border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <CardHeader className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-500/10 to-blue-600/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <span className="text-3xl">🎉</span>
                </div>
                <CardTitle className="text-2xl mb-2">Recreativa</CardTitle>
                <CardDescription className="text-base">
                  Disfruta festivales, conciertos y eventos comunitarios que conectan personas
                </CardDescription>
              </CardHeader>
            </Card>
          </div>

          {/* Stats Section */}
          {user && (
            <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="text-center p-6 rounded-lg bg-card border">
                <div className="text-3xl font-bold text-primary mb-2">
                  <Zap className="w-8 h-8 mx-auto mb-2" />
                </div>
                <p className="text-sm text-muted-foreground">Recomendaciones IA</p>
              </div>
              <div className="text-center p-6 rounded-lg bg-card border">
                <div className="text-3xl font-bold text-primary mb-2">
                  <MapPin className="w-8 h-8 mx-auto mb-2" />
                </div>
                <p className="text-sm text-muted-foreground">3 Localidades</p>
              </div>
              <div className="text-center p-6 rounded-lg bg-card border">
                <div className="text-3xl font-bold text-primary mb-2">
                  <Heart className="w-8 h-8 mx-auto mb-2" />
                </div>
                <p className="text-sm text-muted-foreground">Favoritos Ilimitados</p>
              </div>
              <div className="text-center p-6 rounded-lg bg-card border">
                <div className="text-3xl font-bold text-primary mb-2">
                  <Sparkles className="w-8 h-8 mx-auto mb-2" />
                </div>
                <p className="text-sm text-muted-foreground">Personalizado</p>
              </div>
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.6s ease-out;
        }
        .animate-fade-in-up {
          animation: fade-in-up 0.8s ease-out;
        }
        .animation-delay-200 {
          animation-delay: 0.2s;
          animation-fill-mode: both;
        }
        .animation-delay-400 {
          animation-delay: 0.4s;
          animation-fill-mode: both;
        }
        .animation-delay-600 {
          animation-delay: 0.6s;
          animation-fill-mode: both;
        }
      `}</style>
    </section>
  );
}
