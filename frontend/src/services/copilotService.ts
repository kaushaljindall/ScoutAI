import api from '@/utils/axios';

export interface AIMessage {
  id: string;
  chat_id: string;
  role: 'user' | 'assistant';
  message: string;
  context_used?: any;
  created_at: string;
}

export interface CopilotResponse {
  chat_id: string;
  message: AIMessage;
  suggested_actions: string[];
}

export interface ChatHistory {
  id: string;
  title: string;
  created_at: string;
}

export const copilotService = {
  chat: async (params: { message: string; chat_id?: string; current_context?: any }) => {
    const response = await api.post<CopilotResponse>('/copilot/chat', params);
    return response.data;
  },

  getHistory: async () => {
    const response = await api.get<ChatHistory[]>('/copilot/history');
    return response.data;
  }
};
