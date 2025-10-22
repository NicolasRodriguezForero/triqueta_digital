/**
 * Activity Form component for creating/editing activities (RF-009)
 * Admin only
 */
import { useForm } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Actividad, ActividadCreate, TipoActividad, Localidad, NivelActividad } from "../services/activities";

interface ActivityFormProps {
  initialData?: Actividad;
  onSubmit: (data: ActividadCreate) => void;
  onCancel: () => void;
  isSubmitting?: boolean;
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

export function ActivityForm({ initialData, onSubmit, onCancel, isSubmitting }: ActivityFormProps) {
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm<ActividadCreate>({
    defaultValues: initialData ? {
      titulo: initialData.titulo,
      descripcion: initialData.descripcion,
      tipo: initialData.tipo,
      fecha_inicio: initialData.fecha_inicio.split('T')[0] + 'T' + initialData.fecha_inicio.split('T')[1].substring(0, 5),
      fecha_fin: initialData.fecha_fin ? initialData.fecha_fin.split('T')[0] + 'T' + initialData.fecha_fin.split('T')[1].substring(0, 5) : undefined,
      ubicacion_direccion: initialData.ubicacion_direccion,
      ubicacion_lat: initialData.ubicacion_lat,
      ubicacion_lng: initialData.ubicacion_lng,
      localidad: initialData.localidad,
      precio: initialData.precio,
      es_gratis: initialData.es_gratis,
      nivel_actividad: initialData.nivel_actividad || undefined,
      etiquetas: initialData.etiquetas,
      contacto: initialData.contacto || undefined,
      enlace_externo: initialData.enlace_externo || undefined,
      imagen_url: initialData.imagen_url || undefined,
    } : {
      es_gratis: true,
      precio: 0,
      etiquetas: [],
    }
  });

  const esGratis = watch("es_gratis");
  const etiquetas = watch("etiquetas") || [];

  const handleTagsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const tagsString = e.target.value;
    const tagsArray = tagsString.split(',').map(tag => tag.trim()).filter(tag => tag);
    setValue("etiquetas", tagsArray);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Información Básica</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Título */}
          <div>
            <Label htmlFor="titulo">Título *</Label>
            <Input
              id="titulo"
              {...register("titulo", { required: "Título es requerido", maxLength: 255 })}
              placeholder="Nombre de la actividad"
            />
            {errors.titulo && <p className="text-sm text-red-600 mt-1">{errors.titulo.message}</p>}
          </div>

          {/* Descripción */}
          <div>
            <Label htmlFor="descripcion">Descripción *</Label>
            <textarea
              id="descripcion"
              {...register("descripcion", { required: "Descripción es requerida" })}
              className="w-full min-h-[120px] px-3 py-2 border rounded-md"
              placeholder="Describe la actividad en detalle"
            />
            {errors.descripcion && <p className="text-sm text-red-600 mt-1">{errors.descripcion.message}</p>}
          </div>

          {/* Tipo y Localidad */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="tipo">Tipo *</Label>
              <Select
                value={watch("tipo")}
                onValueChange={(value) => setValue("tipo", value as TipoActividad)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona tipo" />
                </SelectTrigger>
                <SelectContent>
                  {TIPOS.map((tipo) => (
                    <SelectItem key={tipo.value} value={tipo.value}>
                      {tipo.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="localidad">Localidad *</Label>
              <Select
                value={watch("localidad")}
                onValueChange={(value) => setValue("localidad", value as Localidad)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona localidad" />
                </SelectTrigger>
                <SelectContent>
                  {LOCALIDADES.map((loc) => (
                    <SelectItem key={loc.value} value={loc.value}>
                      {loc.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Fechas y Horarios</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="fecha_inicio">Fecha y Hora de Inicio *</Label>
              <Input
                id="fecha_inicio"
                type="datetime-local"
                {...register("fecha_inicio", { required: "Fecha de inicio es requerida" })}
              />
              {errors.fecha_inicio && <p className="text-sm text-red-600 mt-1">{errors.fecha_inicio.message}</p>}
            </div>

            <div>
              <Label htmlFor="fecha_fin">Fecha y Hora de Fin</Label>
              <Input
                id="fecha_fin"
                type="datetime-local"
                {...register("fecha_fin")}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Ubicación</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="ubicacion_direccion">Dirección *</Label>
            <Input
              id="ubicacion_direccion"
              {...register("ubicacion_direccion", { required: "Dirección es requerida" })}
              placeholder="Calle, número, barrio"
            />
            {errors.ubicacion_direccion && <p className="text-sm text-red-600 mt-1">{errors.ubicacion_direccion.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="ubicacion_lat">Latitud *</Label>
              <Input
                id="ubicacion_lat"
                type="number"
                step="any"
                {...register("ubicacion_lat", { 
                  required: "Latitud es requerida",
                  valueAsNumber: true
                })}
                placeholder="4.6097100"
              />
              {errors.ubicacion_lat && <p className="text-sm text-red-600 mt-1">{errors.ubicacion_lat.message}</p>}
            </div>

            <div>
              <Label htmlFor="ubicacion_lng">Longitud *</Label>
              <Input
                id="ubicacion_lng"
                type="number"
                step="any"
                {...register("ubicacion_lng", { 
                  required: "Longitud es requerida",
                  valueAsNumber: true
                })}
                placeholder="-74.0817500"
              />
              {errors.ubicacion_lng && <p className="text-sm text-red-600 mt-1">{errors.ubicacion_lng.message}</p>}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Detalles Adicionales</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Precio y Gratis */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="es_gratis"
                checked={esGratis}
                onCheckedChange={(checked) => setValue("es_gratis", checked as boolean)}
              />
              <Label htmlFor="es_gratis" className="cursor-pointer">
                Actividad gratuita
              </Label>
            </div>

            {!esGratis && (
              <div>
                <Label htmlFor="precio">Precio (COP)</Label>
                <Input
                  id="precio"
                  type="number"
                  step="0.01"
                  {...register("precio", { valueAsNumber: true })}
                  placeholder="0"
                />
              </div>
            )}
          </div>

          {/* Nivel de Actividad */}
          <div>
            <Label htmlFor="nivel_actividad">Nivel de Actividad Física</Label>
            <Select
              value={watch("nivel_actividad") || "ninguno"}
              onValueChange={(value) => setValue("nivel_actividad", value === "ninguno" ? undefined : value as NivelActividad)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecciona nivel (opcional)" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ninguno">Ninguno</SelectItem>
                {NIVELES.map((nivel) => (
                  <SelectItem key={nivel.value} value={nivel.value}>
                    {nivel.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Etiquetas */}
          <div>
            <Label htmlFor="etiquetas">Etiquetas (separadas por comas)</Label>
            <Input
              id="etiquetas"
              defaultValue={etiquetas.join(', ')}
              onChange={handleTagsChange}
              placeholder="arte, cultura, gratuito"
            />
            <p className="text-sm text-gray-500 mt-1">
              Actual: {etiquetas.length > 0 ? etiquetas.join(', ') : 'ninguna'}
            </p>
          </div>

          {/* Contacto */}
          <div>
            <Label htmlFor="contacto">Información de Contacto</Label>
            <Input
              id="contacto"
              {...register("contacto")}
              placeholder="Teléfono o email"
            />
          </div>

          {/* Enlaces */}
          <div>
            <Label htmlFor="enlace_externo">Enlace Externo</Label>
            <Input
              id="enlace_externo"
              type="url"
              {...register("enlace_externo")}
              placeholder="https://..."
            />
          </div>

          <div>
            <Label htmlFor="imagen_url">URL de Imagen</Label>
            <Input
              id="imagen_url"
              type="url"
              {...register("imagen_url")}
              placeholder="https://..."
            />
          </div>
        </CardContent>
      </Card>

      {/* Buttons */}
      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={onCancel} disabled={isSubmitting}>
          Cancelar
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Guardando..." : initialData ? "Actualizar" : "Crear"}
        </Button>
      </div>
    </form>
  );
}
