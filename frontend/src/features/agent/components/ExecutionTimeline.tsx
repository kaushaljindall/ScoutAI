import React from 'react';
import { ToolInvocation } from '../types';
import { CheckCircle2, XCircle, Loader2, Clock } from 'lucide-react';

interface ExecutionTimelineProps {
  invocations: ToolInvocation[];
}

export const ExecutionTimeline: React.FC<ExecutionTimelineProps> = ({ invocations }) => {
  return (
    <div className="space-y-4">
      {invocations.map((inv, index) => {
        let Icon = Clock;
        let colorClass = 'text-gray-500';
        
        if (inv.status === 'Completed') {
          Icon = CheckCircle2;
          colorClass = 'text-green-500';
        } else if (inv.status === 'Failed' || inv.status === 'Cancelled') {
          Icon = XCircle;
          colorClass = 'text-red-500';
        } else if (inv.status === 'Executing') {
          Icon = Loader2;
          colorClass = 'text-blue-500 animate-spin';
        }

        return (
          <div key={inv.id} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className={`p-2 rounded-full bg-white/5 border border-white/10 ${colorClass}`}>
                <Icon className="w-4 h-4" />
              </div>
              {index < invocations.length - 1 && (
                <div className="w-px h-full bg-white/10 my-1" />
              )}
            </div>
            <div className="pb-4 flex-1">
              <h4 className="text-sm font-medium text-white">{inv.tool_name}</h4>
              <p className="text-xs text-white/50">{inv.status}</p>
              {inv.execution_time && (
                <p className="text-xs text-white/40">{inv.execution_time.toFixed(2)}s</p>
              )}
              {inv.error && (
                <p className="text-xs text-red-400 mt-1">{inv.error}</p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
