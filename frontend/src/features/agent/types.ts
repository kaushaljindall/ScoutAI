export type ExecutionState = 
  | "Pending"
  | "Planning"
  | "Executing"
  | "Waiting"
  | "Retrying"
  | "Completed"
  | "Failed"
  | "Cancelled";

export interface ToolInvocation {
  id: string;
  tool_name: string;
  input_params?: Record<string, any>;
  output_result?: Record<string, any>;
  error?: string;
  execution_time?: number;
  status: ExecutionState;
}

export interface ExecutionLog {
  id: string;
  level: string;
  message: string;
  details?: Record<string, any>;
  timestamp: string;
}

export interface AgentExecution {
  id: string;
  agent_name: string;
  status: ExecutionState;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  tool_invocations: ToolInvocation[];
  logs: ExecutionLog[];
}

export interface SearchSession {
  id: string;
  user_id: string;
  original_query: string;
  planner_output?: Record<string, any>;
  execution_time?: number;
  status: ExecutionState;
  errors?: string[];
  created_at: string;
  updated_at: string;
  executions: AgentExecution[];
}
