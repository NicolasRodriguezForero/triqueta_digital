/**
 * Registration form component
 */
import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { useRegister } from "../hooks/useAuth";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";

export function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [nombreCompleto, setNombreCompleto] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const registerMutation = useRegister();

  const validatePassword = (pwd: string): boolean => {
    if (pwd.length < 8) {
      setPasswordError("La contraseña debe tener al menos 8 caracteres");
      return false;
    }
    if (!/\d/.test(pwd)) {
      setPasswordError("La contraseña debe contener al menos un número");
      return false;
    }
    if (!/[a-zA-Z]/.test(pwd)) {
      setPasswordError("La contraseña debe contener al menos una letra");
      return false;
    }
    setPasswordError("");
    return true;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validatePassword(password)) {
      return;
    }

    if (password !== confirmPassword) {
      setPasswordError("Las contraseñas no coinciden");
      return;
    }

    registerMutation.mutate({
      email,
      password,
      nombre_completo: nombreCompleto || undefined,
    });
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Crear Cuenta</CardTitle>
        <CardDescription>Regístrate en Triqueta Digital</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={registerMutation.isPending}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="nombreCompleto">Nombre Completo (opcional)</Label>
            <Input
              id="nombreCompleto"
              type="text"
              placeholder="Tu nombre"
              value={nombreCompleto}
              onChange={(e) => setNombreCompleto(e.target.value)}
              disabled={registerMutation.isPending}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Contraseña</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                if (passwordError) validatePassword(e.target.value);
              }}
              required
              disabled={registerMutation.isPending}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirmar Contraseña</Label>
            <Input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={registerMutation.isPending}
            />
          </div>
          {passwordError && (
            <p className="text-sm text-red-600">{passwordError}</p>
          )}
          {registerMutation.isError && (
            <p className="text-sm text-red-600">
              {registerMutation.error?.message || "Error al registrarse"}
            </p>
          )}
          {registerMutation.isSuccess && (
            <p className="text-sm text-green-600">
              ¡Registro exitoso! Redirigiendo al login...
            </p>
          )}
        </CardContent>
        <CardFooter className="flex flex-col space-y-4 mt-4">
          <Button
            type="submit"
            className="w-full"
            disabled={registerMutation.isPending}
          >
            {registerMutation.isPending ? "Registrando..." : "Crear Cuenta"}
          </Button>
          <p className="text-sm text-center text-gray-600 dark:text-gray-400">
            ¿Ya tienes cuenta?{" "}
            <Link
              to="/login"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Inicia sesión aquí
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
