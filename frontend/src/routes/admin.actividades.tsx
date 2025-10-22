/**
 * Admin page for activity management (RF-009)
 * CRUD operations for activities
 */
import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { Layout } from "../components/Layout";
import { ActivityForm } from "../components/ActivityForm";
import { useActivities, useCreateActivity, useUpdateActivity, useDeleteActivity } from "../hooks/useActivities";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { Actividad, ActividadCreate } from "../services/activities";

export const Route = createFileRoute("/admin/actividades")({
  component: AdminActividadesPage,
});

function AdminActividadesPage() {
  const [isCreating, setIsCreating] = useState(false);
  const [editingActivity, setEditingActivity] = useState<Actividad | null>(null);

  const { data, isLoading } = useActivities({ limit: 100 });
  const createMutation = useCreateActivity();
  const updateMutation = useUpdateActivity(editingActivity?.id || "");
  const deleteMutation = useDeleteActivity();

  const handleCreate = async (data: ActividadCreate) => {
    await createMutation.mutateAsync(data);
    setIsCreating(false);
  };

  const handleUpdate = async (data: ActividadCreate) => {
    if (editingActivity) {
      await updateMutation.mutateAsync(data);
      setEditingActivity(null);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("¿Estás seguro de eliminar esta actividad?")) {
      await deleteMutation.mutateAsync(id);
    }
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Gestión de Actividades
            </h1>
            <p className="text-gray-600">
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

        {/* Activities List */}
        {isLoading ? (
          <div className="text-center py-12">Cargando...</div>
        ) : (
          <div className="grid gap-4">
            {data?.data.map((activity) => (
              <Card key={activity.id}>
                <CardContent className="flex items-center justify-between p-6">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold">{activity.titulo}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {activity.localidad} • {activity.tipo} • {activity.fecha_inicio}
                    </p>
                    <div className="flex gap-2 mt-2">
                      {activity.etiquetas.slice(0, 3).map((tag) => (
                        <span
                          key={tag}
                          className="text-xs bg-gray-100 px-2 py-1 rounded"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setEditingActivity(activity)}
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="destructive"
                      size="sm"
                      onClick={() => handleDelete(activity.id)}
                      disabled={deleteMutation.isPending}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
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
        <Dialog open={!!editingActivity} onOpenChange={(open) => !open && setEditingActivity(null)}>
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
      </div>
    </Layout>
  );
}
