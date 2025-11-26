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
import { Sparkles, Mail, Lock, User, ArrowRight, CheckCircle2, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "./ui/alert";
import { getErrorMessage } from "../lib/error-utils";

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
    <div className="w-full max-w-md mx-auto">
      {/* Decorative background */}
      <div className="relative mb-8">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-accent/10 to-primary/20 rounded-2xl blur-2xl -z-10"></div>
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-accent-foreground mb-4 shadow-lg">
            <Sparkles className="w-8 h-8 text-primary-foreground" />
          </div>
          <h2 className="text-3xl font-bold mb-2 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
            Únete a Triqueta Digital
          </h2>
          <p className="text-muted-foreground">
            Crea tu cuenta y comienza a descubrir
          </p>
        </div>
      </div>

      <Card className="border-2 shadow-xl">
        <CardHeader className="space-y-1 pb-4">
          <CardTitle className="text-2xl">Crear Cuenta</CardTitle>
          <CardDescription>
            Regístrate y accede a recomendaciones personalizadas
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-5">
            <div className="space-y-2">
              <Label htmlFor="email" className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-primary" />
                Email
              </Label>
              <Input
                id="email"
                type="email"
                placeholder="tu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={registerMutation.isPending}
                className="h-11"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="nombreCompleto" className="flex items-center gap-2">
                <User className="w-4 h-4 text-primary" />
                Nombre Completo <span className="text-muted-foreground text-xs font-normal">(opcional)</span>
              </Label>
              <Input
                id="nombreCompleto"
                type="text"
                placeholder="Tu nombre completo"
                value={nombreCompleto}
                onChange={(e) => setNombreCompleto(e.target.value)}
                disabled={registerMutation.isPending}
                className="h-11"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-primary" />
                Contraseña
              </Label>
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
                className="h-11"
              />
              <p className="text-xs text-muted-foreground">
                Mínimo 8 caracteres, al menos una letra y un número
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-primary" />
                Confirmar Contraseña
              </Label>
              <Input
                id="confirmPassword"
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                disabled={registerMutation.isPending}
                className="h-11"
              />
            </div>
            {passwordError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{passwordError}</AlertDescription>
              </Alert>
            )}
            {registerMutation.isError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  {getErrorMessage(registerMutation.error) || "Error al registrarse. Intenta nuevamente."}
                </AlertDescription>
              </Alert>
            )}
            {registerMutation.isSuccess && (
              <Alert variant="success">
                <CheckCircle2 className="h-4 w-4" />
                <AlertDescription>
                  ¡Registro exitoso! Redirigiendo al login...
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
          <CardFooter className="flex flex-col space-y-4 pt-6">
            <Button
              type="submit"
              className="w-full h-11 text-base font-semibold gap-2 group"
              disabled={registerMutation.isPending}
            >
              {registerMutation.isPending ? (
                "Creando cuenta..."
              ) : (
                <>
                  Crear Cuenta
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </Button>
            <p className="text-sm text-center text-muted-foreground">
              ¿Ya tienes cuenta?{" "}
              <Link
                to="/login"
                className="text-primary font-semibold hover:underline inline-flex items-center gap-1"
              >
                Inicia sesión aquí
                <ArrowRight className="w-3 h-3" />
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
