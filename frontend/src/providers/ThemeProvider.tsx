import { useEffect } from "react";
import { useTheme } from "../hooks/useTheme";

interface ThemeProviderProps {
  children: React.ReactNode;
}

/**
 * Provider que aplica la clase 'dark' al elemento HTML
 * según la preferencia del sistema
 */
export function ThemeProvider({ children }: ThemeProviderProps) {
  const theme = useTheme();

  useEffect(() => {
    const root = document.documentElement;
    
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }, [theme]);

  return <>{children}</>;
}
