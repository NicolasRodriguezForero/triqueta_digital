import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ActivityValidationCard } from '@/components/ActivityValidationCard';
import { getPendingActivities, approveActivity, rejectActivity } from '@/services/admin';
import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { useToast } from '@/hooks/use-toast';

export const Route = createFileRoute('/admin/actividades/pendientes')({
  component: PendingActivities,
});

function PendingActivities() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  const navigate = useNavigate();

  const { data: activities = [], isLoading } = useQuery({
    queryKey: ['admin', 'pending-activities'],
    queryFn: () => getPendingActivities(50, 0),
    staleTime: 0, // Always fetch fresh data
  });

  const approveMutation = useMutation({
    mutationFn: approveActivity,
    onSuccess: () => {
      toast({
        title: 'Actividad Aprobada',
        description: 'La actividad ha sido aprobada correctamente',
      });
      queryClient.invalidateQueries({ queryKey: ['admin', 'pending-activities'] });
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'No se pudo aprobar la actividad',
        variant: 'destructive',
      });
    },
  });

  const rejectMutation = useMutation({
    mutationFn: rejectActivity,
    onSuccess: () => {
      toast({
        title: 'Actividad Rechazada',
        description: 'La actividad ha sido rechazada',
      });
      queryClient.invalidateQueries({ queryKey: ['admin', 'pending-activities'] });
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'No se pudo rechazar la actividad',
        variant: 'destructive',
      });
    },
  });

  const handleApprove = (id: string) => {
    if (window.confirm('¿Aprobar esta actividad?')) {
      approveMutation.mutate(id);
    }
  };

  const handleReject = (id: string) => {
    if (window.confirm('¿Rechazar esta actividad?')) {
      rejectMutation.mutate(id);
    }
  };

  const handleView = (id: string) => {
    navigate({ to: `/actividades/${id}` });
  };

  if (isLoading) {
    return (
      <div className="container mx-auto py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Actividades Pendientes</h1>
        <p className="text-muted-foreground mt-2">
          {activities.length} actividades esperando validación
        </p>
      </div>

      {activities.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {activities.map((activity: any) => (
            <ActivityValidationCard
              key={activity.id}
              activity={activity}
              onApprove={handleApprove}
              onReject={handleReject}
              onView={handleView}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-16 bg-muted/50 rounded-lg">
          <p className="text-xl text-muted-foreground">
            🎉 No hay actividades pendientes de validación
          </p>
        </div>
      )}
    </div>
  );
}
