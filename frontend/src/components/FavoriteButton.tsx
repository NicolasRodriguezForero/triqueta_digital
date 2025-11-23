/**
 * FavoriteButton component - Toggle button to add/remove from favorites
 */
import { Button } from "@/components/ui/button";
import { Heart } from "lucide-react";
import { useAddFavorite, useRemoveFavorite, useIsFavorite } from "@/hooks/useFavorites";
import { useAuth } from "@/hooks/useAuth";
import { useNavigate } from "@tanstack/react-router";
import { cn } from "@/lib/utils";

interface FavoriteButtonProps {
  actividadId: string;
  className?: string;
  showLabel?: boolean;
  variant?: "default" | "icon";
}

export function FavoriteButton({
  actividadId,
  className,
  showLabel = false,
  variant = "icon",
}: FavoriteButtonProps) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { data: favoriteStatus, isLoading } = useIsFavorite(actividadId);
  const addFavorite = useAddFavorite();
  const removeFavorite = useRemoveFavorite();

  const isFavorite = favoriteStatus?.is_favorite || false;

  const handleClick = async (e: React.MouseEvent) => {
    e.preventDefault(); // Prevent navigation if inside a link
    e.stopPropagation(); // Prevent parent click handlers

    // Require authentication
    if (!user) {
      navigate({ to: "/login" });
      return;
    }

    try {
      if (isFavorite) {
        await removeFavorite.mutateAsync(actividadId);
      } else {
        await addFavorite.mutateAsync(actividadId);
      }
    } catch (error) {
      // Error handling is done in the mutation hooks
      console.error("Error toggling favorite:", error);
    }
  };

  const isProcessing = addFavorite.isPending || removeFavorite.isPending;

  if (variant === "icon") {
    return (
      <Button
        variant="ghost"
        size="icon"
        onClick={handleClick}
        disabled={isLoading || isProcessing}
        className={cn(
          "transition-all duration-200",
          isFavorite && "text-red-500 hover:text-red-600",
          className
        )}
        title={isFavorite ? "Eliminar de favoritos" : "Agregar a favoritos"}
      >
        <Heart
          className={cn(
            "w-5 h-5 transition-all duration-200",
            isFavorite && "fill-current",
            isProcessing && "animate-pulse"
          )}
        />
      </Button>
    );
  }

  return (
    <Button
      variant={isFavorite ? "default" : "outline"}
      onClick={handleClick}
      disabled={isLoading || isProcessing}
      className={cn(
        "transition-all duration-200",
        isFavorite && "bg-red-500 hover:bg-red-600 text-white",
        className
      )}
    >
      <Heart
        className={cn(
          "mr-2 h-4 w-4 transition-all duration-200",
          isFavorite && "fill-current",
          isProcessing && "animate-pulse"
        )}
      />
      {showLabel && (isFavorite ? "En favoritos" : "Agregar a favoritos")}
    </Button>
  );
}
