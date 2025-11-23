/**
 * Navbar component with authentication state and responsive mobile menu
 */
import { useState } from "react";
import { Link, useLocation } from "@tanstack/react-router";
import { Menu, X, User, LogOut, Sparkles, Heart, LayoutDashboard } from "lucide-react";
import { useCurrentUser, useLogout } from "../hooks/useAuth";
import { Button } from "./ui/button";

export function Navbar() {
  const { data: user, isLoading } = useCurrentUser();
  const logoutMutation = useLogout();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const handleLogout = () => {
    logoutMutation.mutate();
    setIsMobileMenuOpen(false);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  const NavLink = ({ to, children, icon: Icon }: { to: string; children: React.ReactNode; icon?: typeof Sparkles }) => {
    const active = isActive(to);
    return (
      <Link
        to={to}
        className={`relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
          active
            ? "text-primary bg-primary/10"
            : "text-muted-foreground hover:text-foreground hover:bg-accent"
        }`}
        onClick={closeMobileMenu}
      >
        {Icon && <Icon className="w-4 h-4 inline-block mr-2" />}
        {children}
        {active && (
          <span className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 rounded-full bg-primary"></span>
        )}
      </Link>
    );
  };

  return (
    <nav className="border-b bg-card/95 backdrop-blur-sm sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-8">
            <Link
              to="/"
              className="flex items-center gap-2 group"
              onClick={closeMobileMenu}
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center group-hover:scale-110 transition-transform">
                <Sparkles className="w-5 h-5 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
                Triqueta
              </span>
              <span className="text-xl font-bold text-primary">Digital</span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-2">
              <NavLink to="/">Inicio</NavLink>
              <NavLink to="/actividades">Actividades</NavLink>
              {user && (
                <>
                  <NavLink to="/recomendaciones" icon={Sparkles}>
                    Recomendaciones
                  </NavLink>
                  <NavLink to="/favoritos" icon={Heart}>
                    Favoritos
                  </NavLink>
                  <NavLink to="/perfil" icon={User}>
                    Perfil
                  </NavLink>
                  {user.is_admin && (
                    <NavLink to="/admin/dashboard" icon={LayoutDashboard}>
                      Admin
                    </NavLink>
                  )}
                </>
              )}
            </div>
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-3">
            {isLoading ? (
              <div className="h-9 w-24 bg-muted animate-pulse rounded-lg" />
            ) : user ? (
              <>
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-accent/50 border">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center">
                    <User className="h-4 w-4 text-primary-foreground" />
                  </div>
                  <span className="text-sm font-medium hidden lg:inline max-w-[120px] truncate">
                    {user.perfil?.nombre_completo || user.email.split("@")[0]}
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  disabled={logoutMutation.isPending}
                  className="gap-2"
                >
                  <LogOut className="h-4 w-4" />
                  {logoutMutation.isPending ? "Cerrando..." : "Salir"}
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm">
                    Iniciar Sesión
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm" className="gap-2">
                    <Sparkles className="h-4 w-4" />
                    Crear Cuenta
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-label="Toggle menu"
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t bg-card/95 backdrop-blur-sm animate-slide-down">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {user ? (
                <>
                  {/* User Info */}
                  <div className="px-3 py-3 mb-2 rounded-lg bg-accent/50 border">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent-foreground flex items-center justify-center">
                        <User className="h-5 w-5 text-primary-foreground" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-foreground truncate">
                          {user.perfil?.nombre_completo || user.email.split("@")[0]}
                        </p>
                        <p className="text-xs text-muted-foreground truncate">
                          {user.email}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Navigation Links */}
                  <NavLink to="/">Inicio</NavLink>
                  <NavLink to="/actividades">Actividades</NavLink>
                  <NavLink to="/recomendaciones" icon={Sparkles}>
                    Recomendaciones
                  </NavLink>
                  <NavLink to="/favoritos" icon={Heart}>
                    Favoritos
                  </NavLink>
                  <NavLink to="/perfil" icon={User}>
                    Mi Perfil
                  </NavLink>

                  {/* Admin Link */}
                  {user.is_admin && (
                    <NavLink to="/admin/dashboard" icon={LayoutDashboard}>
                      Administración
                    </NavLink>
                  )}

                  {/* Logout Button */}
                  <button
                    onClick={handleLogout}
                    disabled={logoutMutation.isPending}
                    className="w-full text-left px-3 py-2 rounded-lg text-base font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-950/20 transition-colors flex items-center space-x-2 mt-2"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>
                      {logoutMutation.isPending
                        ? "Cerrando sesión..."
                        : "Cerrar Sesión"}
                    </span>
                  </button>
                </>
              ) : (
                <>
                  {/* Auth Buttons for Mobile */}
                  <Link
                    to="/login"
                    className="block w-full"
                    onClick={closeMobileMenu}
                  >
                    <Button variant="outline" className="w-full justify-start">
                      Iniciar Sesión
                    </Button>
                  </Link>
                  <Link
                    to="/register"
                    className="block w-full mt-2"
                    onClick={closeMobileMenu}
                  >
                    <Button className="w-full justify-start gap-2">
                      <Sparkles className="h-4 w-4" />
                      Crear Cuenta
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
      <style>{`
        @keyframes slide-down {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-slide-down {
          animation: slide-down 0.2s ease-out;
        }
      `}</style>
    </nav>
  );
}
