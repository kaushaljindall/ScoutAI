import api from '@/utils/axios';

export interface Business {
  id: string;
  business_name: string;
  category: string;
  website?: string;
  phone?: string;
  email?: string;
  instagram?: string;
  linkedin?: string;
  facebook_url?: string;
  city?: string;
  state?: string;
  country?: string;
  google_rating?: number;
  review_count: number;
  website_status?: string;
  logo_url?: string;
  latitude?: number;
  longitude?: number;
  last_checked?: string;
  source?: string;
  confidence_score?: number;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export const scoutService = {
  searchBusinesses: async (params: { q?: string; category?: string; city?: string; page?: number; size?: number }) => {
    const response = await api.get<PaginatedResponse<Business>>('/scout/search', { params });
    return response.data;
  },
  
  getBusinessById: async (id: string) => {
    const response = await api.get<Business>(`/scout/business/${id}`);
    return response.data;
  },
  
  saveLead: async (data: { business_id: string; status?: string; tags?: string[]; notes?: string }) => {
    const response = await api.post('/scout/save', data);
    return response.data;
  },
  
  deleteLeads: async (ids: string[]) => {
    const response = await api.delete('/scout/delete', { data: ids });
    return response.data;
  },
  
  exportLeads: async () => {
    const response = await api.post('/scout/export', null, { responseType: 'blob' });
    return response.data;
  },

  discoverBusinesses: async (params: { query: string; location?: string; max_results?: number; filters?: any }) => {
    const response = await api.post('/scout/discover', params);
    return response.data;
  },

  getSavedLeads: async () => {
    const response = await api.get('/scout/saved');
    return response.data;
  }
};
