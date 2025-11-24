/**
 * Admin page for activity management (RF-009)
 * CRUD operations for activities
 */
import { useState } from "react";
import { createFileRoute, Outlet, useLocation } from "@tanstack/react-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";
import { ActivityForm } from "../components/ActivityForm";
import {
  useCreateActivity,
  useUpdateActivity,
  useDeleteActivity,
} from "../hooks/useActivities";
import { getAllActivitiesAdmin, getActivityById } from "../services/activities";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ConfirmDialog } from "@/components/ui/confirm-dialog";
import type { Actividad, ActividadCreate } from "../services/activities";

export const Route = createFileRoute("/admin/actividades")({
  component: AdminActividadesLayout,
});

function AdminActividadesLayout() {
  const location = useLocation();

  // If we're on a child route (like /admin/actividades/pendientes), render only the child
  if (location.pathname !== "/admin/actividades") {
    return <Outlet />;
  }

  // Otherwise render the main actividades page
  return <AdminActividadesPage />;
}

type SortField = "titulo" | "tipo" | "localidad" | "fecha_inicio" | "estado" | "precio" | "popularidad";
type SortOrder = "asc" | "desc";

function AdminActividadesPage() {
  const queryClient = useQueryClient();
  const [isCreating, setIsCreating] = useState(false);
  const [editingActivity, setEditingActivity] = useState<Actividad | null>(
    null
  );
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [activityToDelete, setActivityToDelete] = useState<string | null>(null);
  
  // Pagination state
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  
  // Sorting state
  const [sortBy, setSortBy] = useState<SortField>("fecha_inicio");
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");

  // Use admin endpoint to get all activities (including inactive)
  const { data, isLoading } = useQuery({
    queryKey: ["admin-activities", page, pageSize, sortBy, sortOrder],
    queryFn: () => getAllActivitiesAdmin({ 
      page, 
      page_size: pageSize,
      sort_by: sortBy,
      sort_order: sortOrder,
    }),
  });
  
  const createMutation = useCreateActivity();
  const updateMutation = useUpdateActivity(editingActivity?.id || "");
  const deleteMutation = useDeleteActivity();

  const handleCreate = async (data: ActividadCreate) => {
    await createMutation.mutateAsync(data);
    setIsCreating(false);
    queryClient.invalidateQueries({ queryKey: ["admin-activities"] });
  };

  const handleUpdate = async (data: ActividadCreate) => {
    if (editingActivity) {
      await updateMutation.mutateAsync(data);
      setEditingActivity(null);
      queryClient.invalidateQueries({ queryKey: ["admin-activities"] });
    }
  };

  const handleDeleteClick = (id: string) => {
    setActivityToDelete(id);
    setDeleteConfirmOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (activityToDelete) {
      await deleteMutation.mutateAsync(activityToDelete);
      setActivityToDelete(null);
      queryClient.invalidateQueries({ queryKey: ["admin-activities"] });
    }
  };

  const handleSort = (field: SortField) => {
    if (sortBy === field) {
      // Toggle order if same field
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      // Set new field with ascending order
      setSortBy(field);
      setSortOrder("asc");
    }
    setPage(1); // Reset to first page when sorting changes
  };

  const getSortIcon = (field: SortField) => {
    if (sortBy !== field) {
      return <ChevronsUpDown className="w-4 h-4 ml-1 opacity-50" />;
    }
    return sortOrder === "asc" ? (
      <ChevronUp className="w-4 h-4 ml-1" />
    ) : (
      <ChevronDown className="w-4 h-4 ml-1" />
    );
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("es-CO", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatPrice = (precio: number, esGratis: boolean) => {
    if (esGratis) return "Gratis";
    return new Intl.NumberFormat("es-CO", {
      style: "currency",
      currency: "COP",
      minimumFractionDigits: 0,
    }).format(precio);
  };

  const getEstadoBadge = (estado: string) => {
    const styles = {
      activa: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
      pendiente_validacion: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
      rechazada: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
      inactiva: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200",
    };
    
    const labels = {
      activa: "Activa",
      pendiente_validacion: "Pendiente",
      rechazada: "Rechazada",
      inactiva: "Inactiva",
    };

    return (
      <span className={`text-xs px-2 py-1 rounded font-medium ${styles[estado as keyof typeof styles] || styles.inactiva}`}>
        {labels[estado as keyof typeof labels] || estado}
      </span>
    );
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            Gestión de Actividades
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Administra las actividades culturales, deportivas y recreativas
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => setIsCreating(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Nueva Actividad
          </Button>
        </div>
      </div>

      {/* Activities Table */}
      {isLoading ? (
        <div className="text-center py-12">Cargando...</div>
      ) : (
        <div className="space-y-4">
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[300px]">
                    <button
                      onClick={() => handleSort("titulo")}
                      className="flex items-center hover:text-primary transition-colors"
                    >
                      Título
                      {getSortIcon("titulo")}
                    </button>
                  </TableHead>
                  <TableHead>
                    <button
                      onClick={() => handleSort("tipo")}
                      className="flex items-center hover:text-primary transition-colors"
                    >
                      Tipo
                      {getSortIcon("tipo")}
                    </button>
                  </TableHead>
                  <TableHead>
                    <button
                      onClick={() => handleSort("localidad")}
                      className="flex items-center hover:text-primary transition-colors"
                    >
                      Localidad
                      {getSortIcon("localidad")}
                    </button>
                  </TableHead>
                  <TableHead>
                    <button
                      onClick={() => handleSort("fecha_inicio")}
                      className="flex items-center hover:text-primary transition-colors"
                    >
                      Fecha Inicio
                      {getSortIcon("fecha_inicio")}
                    </button>
                  </TableHead>
                  <TableHead>
                    <button
                      onClick={() => handleSort("estado")}
                      className="flex items-center hover:text-primary transition-colors"
                    >
                      Estado
                      {getSortIcon("estado")}
                    </button>
                  </TableHead>
                  <TableHead className="text-right">
                    <button
                      onClick={() => handleSort("precio")}
                      className="flex items-center justify-end hover:text-primary transition-colors ml-auto"
                    >
                      Precio
                      {getSortIcon("precio")}
                    </button>
                  </TableHead>
                  <TableHead className="text-right">
                    <button
                      onClick={() => handleSort("popularidad")}
                      className="flex items-center justify-end hover:text-primary transition-colors ml-auto"
                    >
                      Popularidad
                      {getSortIcon("popularidad")}
                    </button>
                  </TableHead>
                  <TableHead className="w-[100px] text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {!data || data.data.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} className="text-center py-8 text-muted-foreground">
                      No hay actividades disponibles
                    </TableCell>
                  </TableRow>
                ) : (
                  data.data.map((activity) => (
                    <TableRow key={activity.id}>
                      <TableCell className="font-medium">{activity.titulo}</TableCell>
                      <TableCell>
                        <span className="capitalize">{activity.tipo}</span>
                      </TableCell>
                      <TableCell>{activity.localidad}</TableCell>
                      <TableCell>{formatDate(activity.fecha_inicio)}</TableCell>
                      <TableCell>{getEstadoBadge(activity.estado || "inactiva")}</TableCell>
                      <TableCell className="text-right">
                        {formatPrice(activity.precio, activity.es_gratis)}
                      </TableCell>
                      <TableCell className="text-right">
                        {activity.popularidad_normalizada
                          ? (Number(activity.popularidad_normalizada) * 100).toFixed(1) + "%"
                          : "0%"}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={async () => {
                              const fullActivity = await getActivityById(activity.id);
                              setEditingActivity(fullActivity);
                            }}
                          >
                            <Pencil className="w-4 h-4" />
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => handleDeleteClick(activity.id)}
                            disabled={deleteMutation.isPending}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>

          {/* Pagination */}
          {data && (
            <div className="flex items-center justify-between border-t pt-4">
              <div className="text-sm text-muted-foreground">
                Mostrando <span className="font-medium text-foreground">{(page - 1) * pageSize + 1}</span> a{" "}
                <span className="font-medium text-foreground">{Math.min(page * pageSize, data.pagination.total)}</span> de{" "}
                <span className="font-medium text-foreground">{data.pagination.total}</span> actividades
                {data.pagination.total_pages > 1 && (
                  <span className="ml-2">
                    (Página <span className="font-medium text-foreground">{page}</span> de{" "}
                    <span className="font-medium text-foreground">{data.pagination.total_pages}</span>)
                  </span>
                )}
              </div>
              {data.pagination.total_pages > 1 && (
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(page - 1)}
                    disabled={page === 1}
                  >
                    Anterior
                  </Button>
                  <div className="flex items-center gap-1">
                    {Array.from({ length: Math.min(5, data.pagination.total_pages) }, (_, i) => {
                      let pageNum: number;
                      if (data.pagination.total_pages <= 5) {
                        pageNum = i + 1;
                      } else if (page <= 3) {
                        pageNum = i + 1;
                      } else if (page >= data.pagination.total_pages - 2) {
                        pageNum = data.pagination.total_pages - 4 + i;
                      } else {
                        pageNum = page - 2 + i;
                      }
                      return (
                        <Button
                          key={pageNum}
                          variant={page === pageNum ? "default" : "outline"}
                          size="sm"
                          onClick={() => setPage(pageNum)}
                          className="min-w-[40px]"
                        >
                          {pageNum}
                        </Button>
                      );
                    })}
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setPage(page + 1)}
                    disabled={page >= data.pagination.total_pages}
                  >
                    Siguiente
                  </Button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Create Dialog */}
      <Dialog open={isCreating} onOpenChange={setIsCreating}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Nueva Actividad</DialogTitle>
            <DialogDescription>
              Completa el formulario para crear una nueva actividad
            </DialogDescription>
          </DialogHeader>
          <ActivityForm
            onSubmit={handleCreate}
            onCancel={() => setIsCreating(false)}
            isSubmitting={createMutation.isPending}
          />
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog
        open={!!editingActivity}
        onOpenChange={(open) => !open && setEditingActivity(null)}
      >
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Editar Actividad</DialogTitle>
            <DialogDescription>
              Modifica los datos de la actividad
            </DialogDescription>
          </DialogHeader>
          {editingActivity && (
            <ActivityForm
              initialData={editingActivity}
              onSubmit={handleUpdate}
              onCancel={() => setEditingActivity(null)}
              isSubmitting={updateMutation.isPending}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        open={deleteConfirmOpen}
        onOpenChange={setDeleteConfirmOpen}
        onConfirm={handleDeleteConfirm}
        title="Eliminar Actividad"
        description="¿Estás seguro de eliminar esta actividad? Esta acción no se puede deshacer."
        confirmText="Eliminar"
        cancelText="Cancelar"
        variant="destructive"
      />
    </div>
  );
}
