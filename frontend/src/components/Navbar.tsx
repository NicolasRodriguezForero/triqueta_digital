/**
 * Navbar component with authentication state and responsive mobile menu
 */
import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { Menu, X, User, LogOut } from "lucide-react";
import { useCurrentUser, useLogout } from "../hooks/useAuth";
import { Button } from "./ui/button";

export function Navbar() {
  const { data: user, isLoading } = useCurrentUser();
  const logoutMutation = useLogout();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logoutMutation.mutate();
    setIsMobileMenuOpen(false);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <nav className="border-b bg-white sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-8">
            <Link 
              to="/" 
              className="text-xl font-bold text-blue-600 hover:text-blue-700 transition-colors"
              onClick={closeMobileMenu}
            >
              Triqueta Digital
            </Link>
            
            {/* Desktop Navigation */}
            {user && (
              <div className="hidden md:flex space-x-4">
                <Link
                  to="/"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Inicio
                </Link>
                <Link
                  to="/perfil"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Mi Perfil
                </Link>
              </div>
            )}
          </div>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {isLoading ? (
              <div className="h-8 w-20 bg-gray-200 animate-pulse rounded" />
            ) : user ? (
              <>
                <span className="text-sm text-gray-700 flex items-center space-x-2">
                  <User className="h-4 w-4" />
                  <span className="hidden lg:inline">
                    {user.perfil?.nombre_completo || user.email}
                  </span>
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  disabled={logoutMutation.isPending}
                >
                  {logoutMutation.isPending ? "Cerrando..." : "Cerrar Sesión"}
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline" size="sm">
                    Iniciar Sesión
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">
                    Registrarse
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
          <div className="md:hidden border-t">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {user ? (
                <>
                  {/* User Info */}
                  <div className="px-3 py-2 text-sm text-gray-700 border-b">
                    <div className="flex items-center space-x-2">
                      <User className="h-4 w-4" />
                      <span className="font-medium">
                        {user.perfil?.nombre_completo || user.email}
                      </span>
                    </div>
                  </div>
                  
                  {/* Navigation Links */}
                  <Link
                    to="/"
                    className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors"
                    onClick={closeMobileMenu}
                  >
                    Inicio
                  </Link>
                  <Link
                    to="/perfil"
                    className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50 transition-colors"
                    onClick={closeMobileMenu}
                  >
                    Mi Perfil
                  </Link>
                  
                  {/* Logout Button */}
                  <button
                    onClick={handleLogout}
                    disabled={logoutMutation.isPending}
                    className="w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-600 hover:bg-red-50 transition-colors flex items-center space-x-2"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>
                      {logoutMutation.isPending ? "Cerrando sesión..." : "Cerrar Sesión"}
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
                    <Button className="w-full justify-start">
                      Registrarse
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
