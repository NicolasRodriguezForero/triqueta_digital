import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, Eye } from 'lucide-react';

interface ActivityValidationCardProps {
  activity: {
    id: string;
    titulo: string;
    descripcion: string;
    tipo: string;
    localidad: string;
    ubicacion_direccion?: string;
    fecha_inicio?: string;
    fecha_fin?: string;
    precio?: number;
    es_gratis: boolean;
    fuente: string;
    estado?: string;
    created_at?: string;
  };
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
  onView?: (id: string) => void;
}

export function ActivityValidationCard({ activity, onApprove, onReject, onView }: ActivityValidationCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg">{activity.titulo}</CardTitle>
            <CardDescription className="mt-1">
              {activity.tipo} • {activity.localidad}
            </CardDescription>
          </div>
          <div className="flex flex-col gap-1 items-end">
            {activity.estado && (
              <Badge 
                variant={
                  activity.estado === 'activa' ? 'default' :
                  activity.estado === 'pendiente_validacion' ? 'secondary' :
                  activity.estado === 'rechazada' ? 'destructive' : 'outline'
                }
                className="ml-2"
              >
                {activity.estado === 'activa' ? 'Activa' :
                 activity.estado === 'pendiente_validacion' ? 'Pendiente' :
                 activity.estado === 'rechazada' ? 'Rechazada' :
                 activity.estado === 'inactiva' ? 'Inactiva' : activity.estado}
              </Badge>
            )}
            <Badge variant="outline">{activity.fuente}</Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
          {activity.descripcion}
        </p>
        
        {activity.ubicacion_direccion && (
          <p className="text-xs text-muted-foreground mb-4">
            📍 {activity.ubicacion_direccion}
          </p>
        )}
        
        <div className="grid grid-cols-2 gap-4 text-sm mb-4">
          {activity.fecha_inicio && (
            <div>
              <span className="text-muted-foreground">Fecha inicio:</span>
              <p className="font-medium">{new Date(activity.fecha_inicio).toLocaleDateString()}</p>
            </div>
          )}
          <div>
            <span className="text-muted-foreground">Precio:</span>
            <p className="font-medium">
              {activity.es_gratis ? 'Gratuita' : `$${activity.precio?.toLocaleString() || 0}`}
            </p>
          </div>
        </div>

        <div className="flex gap-2">
          {onView && (
            <Button variant="outline" size="sm" onClick={() => onView(activity.id)}>
              <Eye className="h-4 w-4 mr-1" />
              Ver
            </Button>
          )}
          <Button variant="default" size="sm" onClick={() => onApprove(activity.id)} className="bg-green-600 hover:bg-green-700">
            <CheckCircle className="h-4 w-4 mr-1" />
            Aprobar
          </Button>
          <Button variant="destructive" size="sm" onClick={() => onReject(activity.id)}>
            <XCircle className="h-4 w-4 mr-1" />
            Rechazar
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
