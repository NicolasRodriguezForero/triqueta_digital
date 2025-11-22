import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { ETLStatusCard } from '@/components/ETLStatusCard';
import { CSVUploader } from '@/components/CSVUploader';
import { getETLStatus, getETLExecutions, triggerETL } from '@/services/admin';
import { PlayCircle, RefreshCw } from 'lucide-react';
import { createFileRoute } from '@tanstack/react-router';
import { useToast } from '@/hooks/use-toast';
import { ConfirmDialog } from '@/components/ui/confirm-dialog';

export const Route = createFileRoute('/admin/etl')({
  component: AdminETL,
});

function AdminETL() {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  const [triggerConfirmOpen, setTriggerConfirmOpen] = useState(false);
  const [sourceToTrigger, setSourceToTrigger] = useState<string | null>(null);

  const { data: currentStatus, isLoading: statusLoading } = useQuery({
    queryKey: ['etl-status'],
    queryFn: getETLStatus,
    refetchInterval: 5000, // Poll every 5 seconds
    retry: false,
  });

  const { data: executions = [], isLoading: executionsLoading } = useQuery({
    queryKey: ['etl-executions'],
    queryFn: () => getETLExecutions(10, 0),
    refetchInterval: 10000,
  });

  const triggerMutation = useMutation({
    mutationFn: (source: string) => triggerETL(source, {}),
    onSuccess: () => {
      toast({
        title: 'ETL Iniciado',
        description: 'El proceso ETL ha sido iniciado correctamente',
      });
      queryClient.invalidateQueries({ queryKey: ['etl-status'] });
      queryClient.invalidateQueries({ queryKey: ['etl-executions'] });
    },
    onError: () => {
      toast({
        title: 'Error',
        description: 'No se pudo iniciar el proceso ETL',
        variant: 'destructive',
      });
    },
  });

  const handleTriggerClick = (source: string) => {
    setSourceToTrigger(source);
    setTriggerConfirmOpen(true);
  };

  const handleTriggerConfirm = () => {
    if (sourceToTrigger) {
      triggerMutation.mutate(sourceToTrigger);
      setSourceToTrigger(null);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Gestión de ETL</h1>
        <p className="text-muted-foreground mt-2">Control y monitoreo de procesos de extracción de datos</p>
      </div>

      {/* Trigger Buttons */}
      <div className="bg-card rounded-lg border p-6 mb-8">
        <h2 className="text-lg font-semibold mb-4">Iniciar Proceso ETL</h2>
        <div className="flex flex-wrap gap-3">
          <Button
            onClick={() => handleTriggerClick('idrd')}
            disabled={triggerMutation.isPending}
          >
            <PlayCircle className="h-4 w-4 mr-2" />
            Ejecutar ETL - IDRD
          </Button>
          <Button
            variant="outline"
            onClick={() => handleTriggerClick('csv')}
            disabled={triggerMutation.isPending}
          >
            <PlayCircle className="h-4 w-4 mr-2" />
            Ejecutar ETL - CSV
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              queryClient.invalidateQueries({ queryKey: ['etl-status'] });
              queryClient.invalidateQueries({ queryKey: ['etl-executions'] });
            }}
          >
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* CSV Upload */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">Subir Archivo CSV</h2>
        <CSVUploader />
      </div>

      {/* Current Status */}
      {!statusLoading && currentStatus && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold mb-4">Estado Actual</h2>
          <ETLStatusCard {...currentStatus} />
        </div>
      )}

      {/* Execution History */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Historial de Ejecuciones</h2>
        {executionsLoading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        ) : executions.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {executions.map((execution: any) => (
              <ETLStatusCard
                key={execution.id}
                status={execution.status}
                source={execution.source}
                startedAt={execution.started_at}
                finishedAt={execution.finished_at}
                recordsLoaded={execution.records_loaded}
                recordsFailed={execution.records_failed}
                errorMessage={execution.error_message}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-muted-foreground">
            No hay ejecuciones registradas
          </div>
        )}
      </div>

      {/* Trigger Confirmation Dialog */}
      <ConfirmDialog
        open={triggerConfirmOpen}
        onOpenChange={setTriggerConfirmOpen}
        onConfirm={handleTriggerConfirm}
        title="Iniciar Proceso ETL"
        description={
          sourceToTrigger
            ? `¿Estás seguro de iniciar el proceso ETL desde la fuente: ${sourceToTrigger.toUpperCase()}?`
            : "¿Estás seguro de iniciar el proceso ETL?"
        }
        confirmText="Iniciar"
        cancelText="Cancelar"
        variant="default"
      />
    </div>
  );
}
