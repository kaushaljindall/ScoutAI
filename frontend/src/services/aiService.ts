import api from '@/utils/axios';

export interface AIAnalysis {
  id: string;
  business_id: string;
  summary_short: string;
  summary_medium: string;
  summary_long: string;
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  opportunity_score: number;
  confidence_score: number;
  ai_tags: string[];
  estimated_budget: string;
  recommended_services: string[];
}

export const aiService = {
  analyzeBusiness: async (businessId: string): Promise<AIAnalysis> => {
    const response = await api.post(`/ai/analyze/${businessId}`);
    return response.data;
  },

  reanalyzeBusiness: async (businessId: string): Promise<AIAnalysis> => {
    const response = await api.post(`/ai/reanalyze/${businessId}`);
    return response.data;
  },

  getBusinessAnalysis: async (businessId: string): Promise<AIAnalysis> => {
    const response = await api.get(`/ai/business/${businessId}`);
    return response.data;
  },
};
