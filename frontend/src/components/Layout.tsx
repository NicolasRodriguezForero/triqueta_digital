/**
 * Layout component with Navbar and Footer
 */
import { ReactNode } from "react";
import { Link } from "@tanstack/react-router";
import { Navbar } from "./Navbar";
import { Sparkles, Heart, MapPin } from "lucide-react";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />
      <main className="flex-1 flex flex-col">{children}</main>
      <footer className="border-t bg-card/50 backdrop-blur-sm mt-auto">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            {/* Brand Section */}
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-primary-foreground" />
                </div>
                <div>
                  <span className="text-lg font-bold">Triqueta</span>
                  <span className="text-lg font-bold text-primary">
                    {" "}
                    Digital
                  </span>
                </div>
              </div>
              <p className="text-sm text-muted-foreground max-w-xs">
                Conectando comunidades a través de actividades culturales,
                recreativas y deportivas en Bogotá.
              </p>
            </div>

            {/* Quick Links */}
            <div className="space-y-4">
              <h3 className="font-semibold text-foreground">Enlaces Rápidos</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link
                    to="/actividades"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    Explorar Actividades
                  </Link>
                </li>
                <li>
                  <Link
                    to="/recomendaciones"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    Recomendaciones
                  </Link>
                </li>
                <li>
                  <Link
                    to="/favoritos"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    Mis Favoritos
                  </Link>
                </li>
              </ul>
            </div>

            {/* Contact/Info */}
            <div className="space-y-4">
              <h3 className="font-semibold text-foreground">Información</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-primary" />
                  <span>Chapinero, Santa Fe, La Candelaria</span>
                </li>
                <li className="flex items-center gap-2">
                  <Heart className="w-4 h-4 text-primary" />
                  <span>Hecho con ❤️ para Bogotá</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-muted-foreground text-center md:text-left">
              &copy; {new Date().getFullYear()} Triqueta Digital. Todos los
              derechos reservados.
            </p>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>Proyecto académico</span>
              <span>•</span>
              <span>Universidad Sergio Arboleda</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
