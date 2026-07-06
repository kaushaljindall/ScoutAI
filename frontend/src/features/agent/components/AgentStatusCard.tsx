import React from 'react';
import { ExecutionState } from '../types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Loader2, CheckCircle2, XCircle, Clock } from 'lucide-react';

interface AgentStatusCardProps {
  status: ExecutionState;
  title: string;
  description?: string;
}

export const AgentStatusCard: React.FC<AgentStatusCardProps> = ({ status, title, description }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'Pending':
      case 'Waiting':
        return { icon: <Clock className="w-5 h-5 text-yellow-500" />, color: 'bg-yellow-500/10 text-yellow-500' };
      case 'Planning':
      case 'Executing':
      case 'Retrying':
        return { icon: <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />, color: 'bg-blue-500/10 text-blue-500' };
      case 'Completed':
        return { icon: <CheckCircle2 className="w-5 h-5 text-green-500" />, color: 'bg-green-500/10 text-green-500' };
      case 'Failed':
      case 'Cancelled':
        return { icon: <XCircle className="w-5 h-5 text-red-500" />, color: 'bg-red-500/10 text-red-500' };
      default:
        return { icon: <Clock className="w-5 h-5 text-gray-500" />, color: 'bg-gray-500/10 text-gray-500' };
    }
  };

  const config = getStatusConfig();

  return (
    <Card className="bg-black border border-white/10 text-white">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="flex items-center space-x-2">
          {config.icon}
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
        </div>
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${config.color} border-transparent`}>
          {status}
        </span>
      </CardHeader>
      <CardContent>
        {description && <p className="text-xs text-white/50">{description}</p>}
      </CardContent>
    </Card>
  );
};
