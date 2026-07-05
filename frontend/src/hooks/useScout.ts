import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { scoutService } from '@/services/scoutService';

export const scoutKeys = {
  all: ['scout'] as const,
  lists: () => [...scoutKeys.all, 'list'] as const,
  list: (filters: string) => [...scoutKeys.lists(), { filters }] as const,
  details: () => [...scoutKeys.all, 'detail'] as const,
  detail: (id: string) => [...scoutKeys.details(), id] as const,
  savedLeads: () => [...scoutKeys.all, 'savedLeads'] as const,
};

export const useGetSavedLeads = () => {
  return useQuery({
    queryKey: scoutKeys.savedLeads(),
    queryFn: scoutService.getSavedLeads,
  });
};

export const useSearchBusinesses = (filters: any) => {
  return useQuery({
    queryKey: scoutKeys.list(JSON.stringify(filters)),
    queryFn: () => scoutService.searchBusinesses(filters),
    placeholderData: (previousData) => previousData,
  });
};

export const useGetBusiness = (id: string | null) => {
  return useQuery({
    queryKey: scoutKeys.detail(id!),
    queryFn: () => scoutService.getBusinessById(id!),
    enabled: !!id,
  });
};

export const useSaveLead = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: scoutService.saveLead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: scoutKeys.lists() });
    },
  });
};

export const useDeleteLeads = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: scoutService.deleteLeads,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: scoutKeys.lists() });
    },
  });
};

export const useDiscoverBusinesses = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: scoutService.discoverBusinesses,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: scoutKeys.lists() });
    },
  });
};
