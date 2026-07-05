import api from '@/utils/axios';

export interface StructuredMessage {
  opening: string;
  observation: string;
  value_proposition: string;
  cta: string;
  closing: string;
}

export interface AISuggestions {
  best_time: string;
  recommended_channel: string;
  likely_pain_points: string[];
  recommended_service: string;
  reply_probability: string;
  follow_up_day: string;
}

export interface MessageVariation {
  version: string;
  message_type: string;
  structured_content: StructuredMessage;
  full_message: string;
  ai_suggestions: AISuggestions;
}

export interface GenerateMessageRequest {
  message_type: string;
  tone: string;
  language: string;
  length: string;
  cta_style: string;
  personalization_level: string;
  user_context?: any;
}

export const outreachService = {
  generateMessage: async (businessId: string, params: GenerateMessageRequest) => {
    const response = await api.post<{ business_id: string; variations: MessageVariation[] }>(`/outreach/generate-message/${businessId}`, params);
    return response.data;
  },
  regenerateMessage: async (businessId: string, params: GenerateMessageRequest) => {
    const response = await api.post<{ business_id: string; variations: MessageVariation[] }>(`/outreach/regenerate/${businessId}`, params);
    return response.data;
  }
};
