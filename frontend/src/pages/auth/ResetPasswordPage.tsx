import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import api from '@/utils/axios';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

const resetPasswordSchema = z.object({
  password: z.string().min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Must contain at least one number'),
  confirm_password: z.string(),
}).refine((data) => data.password === data.confirm_password, {
  message: "Passwords don't match",
  path: ["confirm_password"],
});

type ResetPasswordValues = z.infer<typeof resetPasswordSchema>;

export default function ResetPasswordPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetPasswordValues>({
    resolver: zodResolver(resetPasswordSchema),
  });

  const onSubmit = async (data: ResetPasswordValues) => {
    setError(null);
    if (!token) {
      setError("Invalid or missing reset token.");
      return;
    }
    
    try {
      await api.post('/auth/reset-password', {
        token,
        new_password: data.password
      });
      setSuccess(true);
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred resetting your password');
    }
  };

  if (!token && !error) {
    return (
      <Card>
        <CardContent className="pt-6 text-center text-red-500">
          Invalid password reset link. Please request a new one.
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Reset your password</CardTitle>
        <CardDescription>Enter a new strong password below</CardDescription>
      </CardHeader>
      <CardContent>
        {success ? (
          <div className="bg-emerald-500/10 text-emerald-500 p-4 rounded-lg flex flex-col items-center justify-center text-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
            <div>
              <p className="font-medium">Password Reset Successfully</p>
              <p className="text-sm opacity-80 mt-1">Redirecting to login...</p>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium leading-none">New Password</label>
              <Input 
                type="password" 
                placeholder="••••••••" 
                {...register('password')}
                error={errors.password?.message}
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium leading-none">Confirm Password</label>
              <Input 
                type="password" 
                placeholder="••••••••" 
                {...register('confirm_password')}
                error={errors.confirm_password?.message}
              />
            </div>
            
            {error && <div className="text-sm font-medium text-red-500 bg-red-500/10 p-3 rounded-md">{error}</div>}
            
            <Button type="submit" className="w-full mt-4" isLoading={isSubmitting}>
              Reset Password
            </Button>
          </form>
        )}
      </CardContent>
    </Card>
  );
}
