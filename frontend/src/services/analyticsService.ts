import api from '@/utils/axios';

export interface DashboardMetrics {
  total_leads: number;
  contacted: number;
  replies: number;
  meetings: number;
  proposals_sent: number;
  deals_won: number;
  lost_deals: number;
  conversion_rate: number;
  expected_revenue: number;
  closed_revenue: number;
}

export interface AIInsight {
  insight: string;
  explanation: string;
  action_type: 'warning' | 'success' | 'info';
}

export interface Goal {
  id: string;
  title: string;
  type: string;
  target_value: number;
  current_value: number;
  status: string;
}

export const analyticsService = {
  getDashboardMetrics: async () => {
    const response = await api.get<DashboardMetrics>('/analytics/dashboard');
    return response.data;
  },

  getInsights: async () => {
    const response = await api.get<AIInsight[]>('/analytics/insights');
    return response.data;
  },

  getGoals: async () => {
    const response = await api.get<Goal[]>('/analytics/goals');
    return response.data;
  },

  createGoal: async (params: any) => {
    const response = await api.post<Goal>('/analytics/goals', params);
    return response.data;
  },

  updateGoal: async (id: string, params: any) => {
    const response = await api.put<Goal>(`/analytics/goals/${id}`, params);
    return response.data;
  }
};
