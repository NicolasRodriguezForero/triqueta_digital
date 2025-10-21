/**
 * Layout component with Navbar and Footer
 */
import { ReactNode } from "react";
import { Navbar } from "./Navbar";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        {children}
      </main>
      <footer className="border-t bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center text-sm text-gray-600">
            <p>&copy; 2025 Triqueta Digital. Todos los derechos reservados.</p>
            <p className="mt-2">
              Conectando actividades culturales, recreativas y deportivas en Bogotá
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
