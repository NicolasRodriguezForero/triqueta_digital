/**
 * ActivityFilters component for filtering activities (RF-007)
 */
import { Filter, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Checkbox } from "@/components/ui/checkbox";
import type { TipoActividad, Localidad, NivelActividad } from "../services/activities";

export interface FilterValues {
  tipo?: TipoActividad;
  localidad?: Localidad;
  es_gratis?: boolean;
  nivel_actividad?: NivelActividad;
}

interface ActivityFiltersProps {
  filters: FilterValues;
  onChange: (filters: FilterValues) => void;
  onClear: () => void;
}

const TIPOS: { value: TipoActividad; label: string }[] = [
  { value: "cultura", label: "Cultura" },
  { value: "deporte", label: "Deporte" },
  { value: "recreacion", label: "Recreación" },
];

const LOCALIDADES: { value: Localidad; label: string }[] = [
  { value: "Chapinero", label: "Chapinero" },
  { value: "Santa Fe", label: "Santa Fe" },
  { value: "La Candelaria", label: "La Candelaria" },
];

const NIVELES: { value: NivelActividad; label: string }[] = [
  { value: "bajo", label: "Bajo" },
  { value: "medio", label: "Medio" },
  { value: "alto", label: "Alto" },
];

export function ActivityFilters({ filters, onChange, onClear }: ActivityFiltersProps) {
  const activeFiltersCount = Object.values(filters).filter(
    (v) => v !== undefined && v !== null
  ).length;

  const updateFilter = <K extends keyof FilterValues>(
    key: K,
    value: FilterValues[K]
  ) => {
    onChange({
      ...filters,
      [key]: value,
    });
  };

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline" className="relative">
          <Filter className="w-4 h-4 mr-2" />
          Filtros
          {activeFiltersCount > 0 && (
            <span className="ml-2 bg-blue-600 text-white text-xs rounded-full px-2 py-0.5">
              {activeFiltersCount}
            </span>
          )}
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-full sm:max-w-md overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Filtrar actividades</SheetTitle>
          <SheetDescription>
            Aplica filtros para encontrar las actividades que más te interesan
          </SheetDescription>
        </SheetHeader>

        <div className="space-y-6 mt-6">
          {/* Tipo de Actividad */}
          <div className="space-y-2">
            <Label htmlFor="tipo">Tipo de actividad</Label>
            <Select
              value={filters.tipo || ""}
              onValueChange={(value: string) =>
                updateFilter("tipo", value ? (value as TipoActividad) : undefined)
              }
            >
              <SelectTrigger id="tipo">
                <SelectValue placeholder="Todos los tipos" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos los tipos</SelectItem>
                {TIPOS.map((tipo) => (
                  <SelectItem key={tipo.value} value={tipo.value}>
                    {tipo.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Localidad */}
          <div className="space-y-2">
            <Label htmlFor="localidad">Localidad</Label>
            <Select
              value={filters.localidad || ""}
              onValueChange={(value: string) =>
                updateFilter("localidad", value ? (value as Localidad) : undefined)
              }
            >
              <SelectTrigger id="localidad">
                <SelectValue placeholder="Todas las localidades" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todas las localidades</SelectItem>
                {LOCALIDADES.map((loc) => (
                  <SelectItem key={loc.value} value={loc.value}>
                    {loc.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Es Gratis */}
          <div className="flex items-center space-x-2">
            <Checkbox
              id="es_gratis"
              checked={filters.es_gratis || false}
              onCheckedChange={(checked: boolean) =>
                updateFilter("es_gratis", checked === true ? true : undefined)
              }
            />
            <Label
              htmlFor="es_gratis"
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
            >
              Solo actividades gratuitas
            </Label>
          </div>

          {/* Nivel de Actividad */}
          <div className="space-y-2">
            <Label htmlFor="nivel">Nivel de actividad física</Label>
            <Select
              value={filters.nivel_actividad || ""}
              onValueChange={(value: string) =>
                updateFilter(
                  "nivel_actividad",
                  value ? (value as NivelActividad) : undefined
                )
              }
            >
              <SelectTrigger id="nivel">
                <SelectValue placeholder="Todos los niveles" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos los niveles</SelectItem>
                {NIVELES.map((nivel) => (
                  <SelectItem key={nivel.value} value={nivel.value}>
                    {nivel.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Clear Filters Button */}
          {activeFiltersCount > 0 && (
            <Button
              variant="outline"
              className="w-full"
              onClick={onClear}
            >
              <X className="w-4 h-4 mr-2" />
              Limpiar filtros
            </Button>
          )}
        </div>
      </SheetContent>
    </Sheet>
  );
}
