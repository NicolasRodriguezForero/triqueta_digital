import { createFileRoute, Navigate } from "@tanstack/react-router";
import { RegisterForm } from "../components/RegisterForm";
import { useIsAuthenticated } from "../hooks/useAuth";

export const Route = createFileRoute("/register")({
  component: RegisterPage,
});

function RegisterPage() {
  const isAuthenticated = useIsAuthenticated();

  // Redirect to home if already authenticated
  if (isAuthenticated) {
    return <Navigate to="/" />;
  }

  return (
    <div className="flex-1 flex items-center justify-center px-4">
      <RegisterForm />
    </div>
  );
}
