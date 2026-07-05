import api from '@/utils/axios';

export interface Task {
  id: string;
  lead_id: string;
  title: string;
  due_date?: string;
  completed: boolean;
  type?: string;
  created_at: string;
}

export interface Conversation {
  id: string;
  lead_id: string;
  type: string;
  message: string;
  sender: string;
  created_at: string;
  analysis?: any;
}

export interface TimelineEvent {
  id: string;
  lead_id: string;
  event_type: string;
  description: string;
  metadata_json?: any;
  created_at: string;
}

export const crmService = {
  updateStatus: async (leadId: string, status: string) => {
    const response = await api.post(`/crm/update-status/${leadId}`, { status });
    return response.data;
  },
  
  addConversation: async (leadId: string, data: { type: string; message: string; sender: string }) => {
    const response = await api.post<Conversation>(`/crm/conversation/${leadId}`, data);
    return response.data;
  },

  getConversations: async (leadId: string) => {
    const response = await api.get<Conversation[]>(`/crm/conversation/${leadId}`);
    return response.data;
  },

  generateReply: async (context: string) => {
    const response = await api.post('/crm/generate-reply', { context });
    return response.data;
  },

  createTask: async (leadId: string, data: { title: string; due_date?: string; type?: string }) => {
    const response = await api.post<Task>(`/crm/task/${leadId}`, data);
    return response.data;
  },

  getTasks: async (leadId?: string) => {
    const response = await api.get<Task[]>('/crm/tasks', { params: { lead_id: leadId } });
    return response.data;
  },
  
  updateTask: async (taskId: string, data: { completed: boolean }) => {
    const response = await api.put<Task>(`/crm/task/${taskId}`, data);
    return response.data;
  },

  getTimeline: async (leadId: string) => {
    const response = await api.get<TimelineEvent[]>(`/crm/timeline/${leadId}`);
    return response.data;
  }
};
