import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react';

interface ETLStatusCardProps {
  status: 'pending' | 'running' | 'success' | 'failed';
  source: string;
  startedAt: string;
  finishedAt?: string;
  recordsLoaded?: number;
  recordsFailed?: number;
  errorMessage?: string;
}

const statusConfig = {
  pending: { label: 'Pendiente', icon: Clock, color: 'bg-gray-500' },
  running: { label: 'En Ejecución', icon: AlertCircle, color: 'bg-blue-500' },
  success: { label: 'Completado', icon: CheckCircle, color: 'bg-green-500' },
  failed: { label: 'Fallido', icon: XCircle, color: 'bg-red-500' },
};

export function ETLStatusCard({ status, source, startedAt, finishedAt, recordsLoaded, recordsFailed, errorMessage }: ETLStatusCardProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">ETL - {source}</CardTitle>
          <Badge className={config.color}>
            <Icon className="h-3 w-3 mr-1" />
            {config.label}
          </Badge>
        </div>
        <CardDescription>
          Iniciado: {new Date(startedAt).toLocaleString()}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {finishedAt && (
            <p className="text-sm text-muted-foreground">
              Finalizado: {new Date(finishedAt).toLocaleString()}
            </p>
          )}
          {recordsLoaded !== undefined && (
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Registros cargados:</span>
              <span className="font-medium text-green-600">{recordsLoaded}</span>
            </div>
          )}
          {recordsFailed !== undefined && recordsFailed > 0 && (
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Registros fallidos:</span>
              <span className="font-medium text-red-600">{recordsFailed}</span>
            </div>
          )}
          {errorMessage && (
            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-800">
              {errorMessage}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
