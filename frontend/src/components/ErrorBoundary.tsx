import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCcw } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
          <div className="max-w-md w-full bg-surface/30 p-8 rounded-2xl border border-border text-center space-y-6">
            <div className="w-16 h-16 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mx-auto">
              <AlertTriangle size={32} />
            </div>
            
            <div>
              <h1 className="text-2xl font-bold tracking-tight mb-2">Something went wrong</h1>
              <p className="text-primary/60 text-sm">
                An unexpected error occurred in the application. Our team has been notified.
              </p>
            </div>
            
            <div className="p-4 bg-background border border-border/50 rounded-lg text-left overflow-auto max-h-32">
              <p className="text-xs font-mono text-red-400">
                {this.state.error?.message || 'Unknown error'}
              </p>
            </div>
            
            <Button 
              className="w-full gap-2" 
              onClick={() => window.location.href = '/dashboard'}
            >
              <RefreshCcw size={16} /> Reload Application
            </Button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
