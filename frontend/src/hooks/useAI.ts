import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { aiService } from '@/services/aiService';

export const aiKeys = {
  all: ['ai'] as const,
  business: (businessId: string) => [...aiKeys.all, 'business', businessId] as const,
};

export const useGetBusinessAnalysis = (businessId: string | null) => {
  return useQuery({
    queryKey: aiKeys.business(businessId!),
    queryFn: () => aiService.getBusinessAnalysis(businessId!),
    enabled: !!businessId,
    retry: false,
  });
};

export const useAnalyzeBusiness = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (businessId: string) => aiService.analyzeBusiness(businessId),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(aiKeys.business(variables), data);
    },
  });
};

export const useReanalyzeBusiness = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (businessId: string) => aiService.reanalyzeBusiness(businessId),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(aiKeys.business(variables), data);
    },
  });
};
