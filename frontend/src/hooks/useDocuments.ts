import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { documentService } from '@/services/documentService';

export const documentKeys = {
  all: ['documents'] as const,
  list: () => [...documentKeys.all, 'list'] as const,
  detail: (id: string) => [...documentKeys.all, 'detail', id] as const,
};

export const useGetDocuments = () => {
  return useQuery({
    queryKey: documentKeys.list(),
    queryFn: documentService.getDocuments,
  });
};

export const useGetDocument = (id: string | null) => {
  return useQuery({
    queryKey: documentKeys.detail(id!),
    queryFn: () => documentService.getDocument(id!),
    enabled: !!id,
  });
};

export const useGenerateDocument = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: documentService.generateDocument,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: documentKeys.list() });
    },
  });
};

export const useUpdateDocument = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, params }: { id: string; params: any }) => documentService.updateDocument(id, params),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: documentKeys.detail(variables.id) });
      queryClient.invalidateQueries({ queryKey: documentKeys.list() });
    },
  });
};
