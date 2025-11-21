import apiClient from './api';

// Dashboard
export const getDashboardMetrics = async () => {
  const { data } = await apiClient.get('/admin/dashboard');
  return data;
};

// ETL Management
export const getETLStatus = async () => {
  const { data } = await apiClient.get('/admin/etl/status');
  return data;
};

export const getETLExecutions = async (limit: number = 20, offset: number = 0) => {
  const { data } = await apiClient.get('/admin/etl/executions', {
    params: { limit, offset }
  });
  return data;
};

export const getETLExecutionDetail = async (executionId: number) => {
  const { data } = await apiClient.get(`/admin/etl/executions/${executionId}`);
  return data;
};

export const triggerETL = async (source: string, config?: any) => {
  const { data } = await apiClient.post('/admin/etl/run', {
    source,
    config
  });
  return data;
};

// Activity Validation
export const getPendingActivities = async (limit: number = 50, offset: number = 0) => {
  const { data } = await apiClient.get('/admin/actividades/pendientes', {
    params: { limit, offset }
  });
  return data;
};

export const approveActivity = async (activityId: number) => {
  const { data } = await apiClient.post('/admin/actividades/aprobar', {
    activity_id: activityId
  });
  return data;
};

export const rejectActivity = async (activityId: number) => {
  const { data } = await apiClient.post('/admin/actividades/rechazar', {
    activity_id: activityId
  });
  return data;
};

