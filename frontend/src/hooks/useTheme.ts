import { useEffect, useState } from "react";

type Theme = "light" | "dark";

/**
 * Hook para detectar y gestionar el tema del sistema
 * @returns El tema actual (light o dark)
 */
export function useTheme(): Theme {
  const [theme, setTheme] = useState<Theme>(() => {
    // Detectar preferencia inicial del sistema
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  });

  useEffect(() => {
    // Listener para cambios en la preferencia del sistema
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
    
    const handleChange = (e: MediaQueryListEvent) => {
      setTheme(e.matches ? "dark" : "light");
    };

    // Agregar listener
    mediaQuery.addEventListener("change", handleChange);

    // Cleanup
    return () => {
      mediaQuery.removeEventListener("change", handleChange);
    };
  }, []);

  return theme;
}
