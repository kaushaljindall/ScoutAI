import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { copilotService } from '@/services/copilotService';

export const copilotKeys = {
  all: ['copilot'] as const,
  history: () => [...copilotKeys.all, 'history'] as const,
};

export const useGetCopilotHistory = () => {
  return useQuery({
    queryKey: copilotKeys.history(),
    queryFn: copilotService.getHistory,
  });
};

export const useCopilotChat = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: copilotService.chat,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: copilotKeys.history() });
    },
  });
};
