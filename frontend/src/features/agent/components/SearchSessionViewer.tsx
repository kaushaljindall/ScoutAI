import React from 'react';
import { SearchSession } from '../types';
import { AgentStatusCard } from './AgentStatusCard';
import { ProgressBar } from './ProgressBar';
import { ExecutionTimeline } from './ExecutionTimeline';
import { ExecutionLogPanel } from './ExecutionLogPanel';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';

interface SearchSessionViewerProps {
  session: SearchSession | null;
  isLoading?: boolean;
}

export const SearchSessionViewer: React.FC<SearchSessionViewerProps> = ({ session, isLoading }) => {
  if (isLoading) {
    return <div className="text-white/50 text-center py-8">Loading session...</div>;
  }

  if (!session) {
    return null;
  }

  // Calculate progress safely
  const currentStage = session.status === 'Pending' ? 0 :
                       session.status === 'Planning' ? 1 :
                       session.status === 'Executing' ? 2 :
                       session.status === 'Waiting' ? 3 :
                       (session.status === 'Completed' || session.status === 'Failed' || session.status === 'Cancelled') ? 4 : 0;
                       
  const totalStages = 4;

  const currentExecution = session.executions?.[0] || { tool_invocations: [], logs: [] };

  return (
    <div className="space-y-6 max-w-4xl mx-auto p-4">
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold text-white tracking-tight">Agent Execution Session</h2>
        <p className="text-sm text-white/50 font-mono">{session.id}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <AgentStatusCard 
          title="Overall Status" 
          status={session.status} 
          description={session.original_query}
        />
        <div className="md:col-span-2 flex flex-col justify-center space-y-2 px-4 bg-white/5 border border-white/10 rounded-xl">
          <div className="flex justify-between text-xs text-white/70">
            <span>Understanding</span>
            <span>Planning</span>
            <span>Executing</span>
            <span>Validating</span>
          </div>
          <ProgressBar currentStage={currentStage} totalStages={totalStages} status={session.status} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-black border border-white/10 text-white">
          <CardHeader>
            <CardTitle className="text-lg">Execution Timeline</CardTitle>
          </CardHeader>
          <CardContent>
            {currentExecution.tool_invocations.length > 0 ? (
              <ExecutionTimeline invocations={currentExecution.tool_invocations} />
            ) : (
              <p className="text-white/40 text-sm italic">No tools have been invoked yet.</p>
            )}
          </CardContent>
        </Card>

        <div className="space-y-6">
          {session.planner_output && (
            <Card className="bg-black border border-white/10 text-white">
              <CardHeader>
                <CardTitle className="text-lg">Execution Plan</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between border-b border-white/10 pb-2">
                    <span className="text-white/50">Intent</span>
                    <span className="font-medium">{session.planner_output.intent}</span>
                  </div>
                  <div className="flex justify-between border-b border-white/10 pb-2">
                    <span className="text-white/50">Target</span>
                    <span className="font-medium">{session.planner_output.industry} - {session.planner_output.location}</span>
                  </div>
                  <div className="pt-2">
                    <span className="text-white/50 block mb-2">Required Tools</span>
                    <div className="flex flex-wrap gap-2">
                      {session.planner_output.requires?.map((tool: string) => (
                        <span key={tool} className="px-2 py-1 bg-white/10 rounded-md text-xs">
                          {tool}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          <ExecutionLogPanel logs={currentExecution.logs} />
        </div>
      </div>
    </div>
  );
};
