/**
 * Login form component
 */
import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { useLogin } from "../hooks/useAuth";
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
import { Sparkles, Mail, Lock, ArrowRight, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "./ui/alert";

export function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const loginMutation = useLogin();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loginMutation.mutate({ email, password });
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
            ¡Bienvenido de vuelta!
          </h2>
          <p className="text-muted-foreground">
            Continúa descubriendo actividades increíbles
          </p>
        </div>
      </div>

      <Card className="border-2 shadow-xl">
        <CardHeader className="space-y-1 pb-4">
          <CardTitle className="text-2xl">Iniciar Sesión</CardTitle>
          <CardDescription>
            Ingresa tus credenciales para acceder a tu cuenta
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
                disabled={loginMutation.isPending}
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
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loginMutation.isPending}
                className="h-11"
              />
            </div>
            {loginMutation.isError && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  {loginMutation.error?.message || "Error al iniciar sesión. Verifica tus credenciales."}
                </AlertDescription>
              </Alert>
            )}
          </CardContent>
          <CardFooter className="flex flex-col space-y-4 pt-6">
            <Button
              type="submit"
              className="w-full h-11 text-base font-semibold gap-2 group"
              disabled={loginMutation.isPending}
            >
              {loginMutation.isPending ? (
                "Iniciando sesión..."
              ) : (
                <>
                  Iniciar Sesión
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </Button>
            <p className="text-sm text-center text-muted-foreground">
              ¿No tienes cuenta?{" "}
              <Link 
                to="/register" 
                className="text-primary font-semibold hover:underline inline-flex items-center gap-1"
              >
                Regístrate aquí
                <ArrowRight className="w-3 h-3" />
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
