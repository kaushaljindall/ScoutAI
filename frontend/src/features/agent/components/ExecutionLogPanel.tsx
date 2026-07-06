import React from 'react';
import { ExecutionLog } from '../types';

interface ExecutionLogPanelProps {
  logs: ExecutionLog[];
}

export const ExecutionLogPanel: React.FC<ExecutionLogPanelProps> = ({ logs }) => {
  return (
    <div className="bg-black border border-white/10 rounded-lg p-4 font-mono text-xs">
      <h3 className="text-white mb-2 font-sans font-medium text-sm">Execution Logs</h3>
      <div className="h-64 w-full rounded-md overflow-y-auto pr-2">
        {logs.length === 0 ? (
          <p className="text-white/40 italic">No logs available yet...</p>
        ) : (
          <div className="space-y-1">
            {logs.map((log) => (
              <div key={log.id} className="flex gap-2">
                <span className="text-white/40 shrink-0">
                  {new Date(log.timestamp).toLocaleTimeString()}
                </span>
                <span className={`shrink-0 ${
                  log.level === 'ERROR' ? 'text-red-400' : 
                  log.level === 'WARN' ? 'text-yellow-400' : 
                  'text-blue-400'
                }`}>
                  [{log.level}]
                </span>
                <span className="text-white/80">{log.message}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
