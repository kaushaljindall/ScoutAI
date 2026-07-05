import api from '@/utils/axios';

export interface Document {
  id: string;
  user_id: string;
  lead_id?: string;
  title: string;
  type: string;
  content: string;
  status: string;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentTemplate {
  id: string;
  user_id: string;
  name: string;
  category: string;
  content: string;
  created_at: string;
}

export const documentService = {
  getDocuments: async () => {
    const response = await api.get<Document[]>('/documents');
    return response.data;
  },

  getDocument: async (id: string) => {
    const response = await api.get<Document>(`/documents/${id}`);
    return response.data;
  },

  generateDocument: async (params: { lead_id: string; type: string; context?: any }) => {
    const response = await api.post<Document>('/documents/generate', params);
    return response.data;
  },

  updateDocument: async (id: string, params: { title?: string; content?: string; status?: string }) => {
    const response = await api.put<Document>(`/documents/${id}`, params);
    return response.data;
  },

  deleteDocument: async (id: string) => {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  }
};
