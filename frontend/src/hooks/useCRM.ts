import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { crmService } from '@/services/crmService';

export const crmKeys = {
  all: ['crm'] as const,
  conversations: (leadId: string) => [...crmKeys.all, 'conversations', leadId] as const,
  tasks: (leadId?: string) => [...crmKeys.all, 'tasks', leadId] as const,
  timeline: (leadId: string) => [...crmKeys.all, 'timeline', leadId] as const,
};

export const useGetConversations = (leadId: string | null) => {
  return useQuery({
    queryKey: crmKeys.conversations(leadId!),
    queryFn: () => crmService.getConversations(leadId!),
    enabled: !!leadId,
  });
};

export const useGetTasks = (leadId?: string) => {
  return useQuery({
    queryKey: crmKeys.tasks(leadId),
    queryFn: () => crmService.getTasks(leadId),
  });
};

export const useGetTimeline = (leadId: string | null) => {
  return useQuery({
    queryKey: crmKeys.timeline(leadId!),
    queryFn: () => crmService.getTimeline(leadId!),
    enabled: !!leadId,
  });
};

export const useUpdateLeadStatus = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ leadId, status }: { leadId: string; status: string }) => 
      crmService.updateStatus(leadId, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['savedLeads'] });
    },
  });
};
