/**
 * Toast notifications hook - Simple implementation without external dependencies
 */

export type ToastVariant = "default" | "destructive" | "success";

export interface ToastOptions {
  title?: string;
  description?: string;
  variant?: ToastVariant;
  duration?: number;
}

export function useToast() {
  const toast = ({ title, description, variant = "default" }: ToastOptions) => {
    // Simple console log for now - can be replaced with actual toast library later
    const message = description ? `${title}: ${description}` : title;
    
    if (variant === "destructive") {
      console.error(message);
    } else if (variant === "success") {
      console.log("✅", message);
    } else {
      console.log(message);
    }
  };

  return { toast };
}
