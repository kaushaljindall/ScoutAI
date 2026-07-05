import { useMutation } from '@tanstack/react-query';
import { outreachService, type GenerateMessageRequest } from '@/services/outreachService';

export const useGenerateMessage = () => {
  return useMutation({
    mutationFn: ({ businessId, params }: { businessId: string; params: GenerateMessageRequest }) => 
      outreachService.generateMessage(businessId, params),
  });
};

export const useRegenerateMessage = () => {
  return useMutation({
    mutationFn: ({ businessId, params }: { businessId: string; params: GenerateMessageRequest }) => 
      outreachService.regenerateMessage(businessId, params),
  });
};
