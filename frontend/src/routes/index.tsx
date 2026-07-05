import { createBrowserRouter } from 'react-router-dom';
import RootLayout from '@/layouts/RootLayout';
import AuthLayout from '@/layouts/AuthLayout';
import DashboardLayout from '@/layouts/DashboardLayout';
import ProtectedRoute from '@/components/ProtectedRoute';

// Lazy loading or direct imports
import LandingPage from '@/pages/LandingPage';
import LoginPage from '@/pages/auth/LoginPage';
import RegisterPage from '@/pages/auth/RegisterPage';
import ForgotPasswordPage from '@/pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '@/pages/auth/ResetPasswordPage';
import DashboardPage from '@/pages/dashboard/DashboardPage';
import ScoutPage from '@/pages/dashboard/ScoutPage';
import OutreachPage from '@/pages/dashboard/OutreachPage';
import CRMPage from '@/pages/dashboard/CRMPage';
import LeadCRMPage from '@/pages/dashboard/LeadCRMPage';
import CopilotPage from '@/pages/dashboard/CopilotPage';
import DocumentsPage from '@/pages/dashboard/DocumentsPage';
import DocumentEditorPage from '@/pages/dashboard/DocumentEditorPage';
import NotFoundPage from '@/pages/NotFoundPage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <NotFoundPage />,
    children: [
      {
        index: true,
        element: <LandingPage />,
      },
    ],
  },
  {
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'register',
        element: <RegisterPage />,
      },
      {
        path: 'forgot-password',
        element: <ForgotPasswordPage />,
      },
      {
        path: 'reset-password',
        element: <ResetPasswordPage />,
      },
    ],
  },
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: 'scout',
        element: <ScoutPage />,
      },
      {
        path: 'outreach/:id',
        element: <OutreachPage />,
      },
      {
        path: 'crm',
        element: <CRMPage />,
      },
      {
        path: 'crm/:id',
        element: <LeadCRMPage />,
      },
      {
        path: 'copilot',
        element: <CopilotPage />,
      },
      {
        path: 'documents',
        element: <DocumentsPage />,
      },
      {
        path: 'documents/:id',
        element: <DocumentEditorPage />,
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);
