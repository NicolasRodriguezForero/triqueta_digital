import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Dashboard
export const getDashboardMetrics = async () => {
  const { data } = await axios.get(`${API_URL}/admin/dashboard`);
  return data;
};

// ETL Management
export const getETLStatus = async () => {
  const { data } = await axios.get(`${API_URL}/admin/etl/status`);
  return data;
};

export const getETLExecutions = async (limit: number = 20, offset: number = 0) => {
  const { data } = await axios.get(`${API_URL}/admin/etl/executions`, {
    params: { limit, offset }
  });
  return data;
};

export const getETLExecutionDetail = async (executionId: number) => {
  const { data } = await axios.get(`${API_URL}/admin/etl/executions/${executionId}`);
  return data;
};

export const triggerETL = async (source: string, config?: any) => {
  const { data } = await axios.post(`${API_URL}/admin/etl/run`, {
    source,
    config
  });
  return data;
};

// Activity Validation
export const getPendingActivities = async (limit: number = 50, offset: number = 0) => {
  const { data } = await axios.get(`${API_URL}/admin/actividades/pendientes`, {
    params: { limit, offset }
  });
  return data;
};

export const approveActivity = async (activityId: number) => {
  const { data } = await axios.post(`${API_URL}/admin/actividades/aprobar`, {
    activity_id: activityId
  });
  return data;
};

export const rejectActivity = async (activityId: number) => {
  const { data } = await axios.post(`${API_URL}/admin/actividades/rechazar`, {
    activity_id: activityId
  });
  return data;
};
