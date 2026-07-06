import React from 'react';
import { ExecutionState } from '../types';

interface ProgressBarProps {
  currentStage: number;
  totalStages: number;
  status: ExecutionState;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ currentStage, totalStages, status }) => {
  const percentage = Math.min(100, Math.max(0, (currentStage / totalStages) * 100));
  
  let colorClass = 'bg-blue-500';
  if (status === 'Completed') colorClass = 'bg-green-500';
  if (status === 'Failed' || status === 'Cancelled') colorClass = 'bg-red-500';

  return (
    <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
      <div 
        className={`h-full ${colorClass} transition-all duration-500 ease-in-out`} 
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
};
