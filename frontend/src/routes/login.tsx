import { createFileRoute, Navigate } from "@tanstack/react-router";
import { LoginForm } from "../components/LoginForm";
import { useIsAuthenticated } from "../hooks/useAuth";

export const Route = createFileRoute("/login")({
  component: LoginPage,
});

function LoginPage() {
  const isAuthenticated = useIsAuthenticated();

  // Redirect to home if already authenticated
  if (isAuthenticated) {
    return <Navigate to="/" />;
  }

  return (
    <div className="flex-1 flex items-center justify-center px-4">
      <LoginForm />
    </div>
  );
}
