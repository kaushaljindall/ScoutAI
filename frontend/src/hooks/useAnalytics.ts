import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { analyticsService } from '@/services/analyticsService';

export const analyticsKeys = {
  all: ['analytics'] as const,
  dashboard: () => [...analyticsKeys.all, 'dashboard'] as const,
  insights: () => [...analyticsKeys.all, 'insights'] as const,
  goals: () => [...analyticsKeys.all, 'goals'] as const,
};

export const useGetDashboardMetrics = () => {
  return useQuery({
    queryKey: analyticsKeys.dashboard(),
    queryFn: analyticsService.getDashboardMetrics,
  });
};

export const useGetInsights = () => {
  return useQuery({
    queryKey: analyticsKeys.insights(),
    queryFn: analyticsService.getInsights,
  });
};

export const useGetGoals = () => {
  return useQuery({
    queryKey: analyticsKeys.goals(),
    queryFn: analyticsService.getGoals,
  });
};

export const useCreateGoal = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: analyticsService.createGoal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analyticsKeys.goals() });
    },
  });
};
