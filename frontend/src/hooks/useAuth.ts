import { useMutation } from '@tanstack/react-query';
import api from '@/utils/axios';
import { useAuthStore } from '@/store/authStore';

export const useLogin = () => {
  const setTokens = useAuthStore((state) => state.setTokens);
  const setUser = useAuthStore((state) => state.setUser);

  return useMutation({
    mutationFn: async (data: URLSearchParams) => {
      const response = await api.post('/auth/login', data, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      return response.data;
    },
    onSuccess: async (data) => {
      setTokens(data.access_token, data.refresh_token);
      const userResponse = await api.get('/auth/me', {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });
      setUser(userResponse.data);
    },
  });
};

export const useRegister = () => {
  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/auth/register', data);
      return response.data;
    },
  });
};

export const useForgotPassword = () => {
  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/auth/forgot-password', data);
      return response.data;
    },
  });
};

export const useResetPassword = () => {
  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/auth/reset-password', data);
      return response.data;
    },
  });
};

export const useLogout = () => {
  const logoutAction = useAuthStore((state) => state.logout);
  const refreshToken = useAuthStore((state) => state.refreshToken);

  return useMutation({
    mutationFn: async () => {
      if (refreshToken) {
        await api.post('/auth/logout', { refresh_token: refreshToken });
      }
    },
    onSettled: () => {
      logoutAction();
    },
  });
};
