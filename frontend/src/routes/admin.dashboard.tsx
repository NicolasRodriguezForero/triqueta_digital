import { useQuery } from '@tanstack/react-query';
import { MetricCard } from '@/components/MetricCard';
import { ChartCard } from '@/components/ChartCard';
import { getDashboardMetrics } from '@/services/admin';
import { Users, Calendar, Heart, Database } from 'lucide-react';
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/admin/dashboard')({
  component: AdminDashboard,
});

function AdminDashboard() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: getDashboardMetrics,
    refetchInterval: 60000, // Refetch every minute
  });

  if (isLoading) {
    return (
      <div className="container mx-auto py-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (!metrics) return null;

  // Prepare chart data
  const activityByLocalityData = Object.entries(metrics.activities.by_locality || {}).map(([name, value]) => ({
    name,
    value: value as number
  }));

  const activityByTypeData = Object.entries(metrics.activities.by_type || {}).map(([name, value]) => ({
    name,
    value: value as number
  }));

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard Administrativo</h1>
        <p className="text-muted-foreground mt-2">Vista general de métricas y estadísticas</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <MetricCard
          title="Total Usuarios"
          value={metrics.users.total}
          description={`${metrics.users.active} activos`}
          icon={Users}
        />
        <MetricCard
          title="Total Actividades"
          value={metrics.activities.total}
          description="En el sistema"
          icon={Calendar}
        />
        <MetricCard
          title="Favoritos"
          value={metrics.engagement.total_favorites}
          description="Total guardados"
          icon={Heart}
        />
        <MetricCard
          title="Ejecuciones ETL"
          value={metrics.etl.total_executions}
          description={`${metrics.etl.success_rate}% éxito`}
          icon={Database}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {activityByLocalityData.length > 0 && (
          <ChartCard
            title="Actividades por Localidad"
            description="Distribución geográfica"
            data={activityByLocalityData}
            type="pie"
          />
        )}
        {activityByTypeData.length > 0 && (
          <ChartCard
            title="Actividades por Tipo"
            description="Categorías disponibles"
            data={activityByTypeData}
            type="bar"
            nameKey="name"
            dataKey="value"
          />
        )}
      </div>

      {/* Top Activities */}
      <div className="bg-card rounded-lg border p-6">
        <h2 className="text-xl font-semibold mb-4">Top 10 Actividades Populares</h2>
        <div className="space-y-3">
          {metrics.engagement.top_activities.map((activity: any, index: number) => (
            <div key={activity.id} className="flex items-center justify-between p-3 bg-muted/50 rounded">
              <div className="flex items-center gap-3">
                <span className="font-bold text-lg text-muted-foreground">#{index + 1}</span>
                <span className="font-medium">{activity.titulo}</span>
              </div>
              <div className="flex gap-4 text-sm text-muted-foreground">
                <span>❤️ {activity.total_favoritos}</span>
                <span>👁️ {Math.round(activity.total_vistas * 10)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
