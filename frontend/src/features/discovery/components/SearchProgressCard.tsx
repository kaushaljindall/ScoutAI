import React from 'react';

interface SearchProgressCardProps {
  stage: string;
  message: string;
  totalResults: number;
  duration?: number;
  isFinished: boolean;
}

const STAGE_LABELS: Record<string, string> = {
  planning: 'Planning Search...',
  running: 'Running Providers...',
  merging: 'Merging Results...',
  completed: 'Search Complete',
};

const STAGE_STEPS = ['planning', 'running', 'merging', 'completed'];

export const SearchProgressCard: React.FC<SearchProgressCardProps> = ({
  stage,
  message,
  totalResults,
  duration,
  isFinished,
}) => {
  const currentStep = STAGE_STEPS.indexOf(stage);

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm p-5 space-y-4">
      {/* Stage Steps */}
      <div className="flex items-center gap-0">
        {STAGE_STEPS.map((s, i) => {
          const isActive = i === currentStep;
          const isDone = i < currentStep || isFinished;
          return (
            <React.Fragment key={s}>
              <div className="flex flex-col items-center gap-1">
                <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-300 ${
                  isDone ? 'bg-green-500 text-white' :
                  isActive ? 'bg-blue-500 text-white animate-pulse' :
                  'bg-white/10 text-white/30'
                }`}>
                  {isDone ? '✓' : i + 1}
                </div>
                <span className={`text-[10px] whitespace-nowrap ${
                  isActive ? 'text-blue-400' : isDone ? 'text-green-400' : 'text-white/30'
                }`}>
                  {STAGE_LABELS[s]}
                </span>
              </div>
              {i < STAGE_STEPS.length - 1 && (
                <div className={`flex-1 h-px mb-5 mx-1 transition-all duration-500 ${
                  i < currentStep || isFinished ? 'bg-green-500/50' : 'bg-white/10'
                }`} />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Stats Row */}
      <div className="flex items-center justify-between text-sm">
        <p className="text-white/70">{message}</p>
        <div className="flex items-center gap-4 text-xs text-white/50">
          {totalResults > 0 && (
            <span className="text-green-400 font-semibold">{totalResults} found</span>
          )}
          {duration != null && (
            <span>{duration.toFixed(1)}s</span>
          )}
        </div>
      </div>
    </div>
  );
};
