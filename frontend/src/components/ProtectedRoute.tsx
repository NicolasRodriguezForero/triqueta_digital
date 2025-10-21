/**
 * ProtectedRoute component
 * Redirects to login if user is not authenticated
 */
import { ReactNode, useEffect } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "../contexts/AuthContext";

interface ProtectedRouteProps {
  children: ReactNode;
  requireAdmin?: boolean;
}

/**
 * Wrapper component for protected routes
 * Redirects to /login if not authenticated
 * Optionally checks for admin role
 */
export function ProtectedRoute({ children, requireAdmin = false }: ProtectedRouteProps) {
  const { user, isLoading, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Redirect to login if not authenticated
      navigate({ to: "/login", search: { redirect: window.location.pathname } });
    } else if (!isLoading && requireAdmin && user && !user.is_admin) {
      // Redirect to home if user is not admin
      navigate({ to: "/" });
    }
  }, [isLoading, isAuthenticated, requireAdmin, user, navigate]);

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Don't render children if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  // Don't render children if admin required but user is not admin
  if (requireAdmin && (!user || !user.is_admin)) {
    return null;
  }

  // Render children if authenticated (and admin if required)
  return <>{children}</>;
}
