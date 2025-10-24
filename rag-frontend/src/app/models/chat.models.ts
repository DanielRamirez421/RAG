export interface QueryRequest {
  userQuestion: string;
  model: string;
  temperature: number;
  context?: string;
}

export interface Source {
  title: string;
  content: string;
  score: number;
}

export interface QueryResponse {
  answer: string;
  selected_model: string;
  temperature: number;
  context: string;
  sources: Source[];
}

export interface ChatMessage {
  content: string;
  isUser: boolean;
  timestamp: Date;
  sources?: Source[];
  model?: string;
  temperature?: number;
  processingTime?: number; // Tiempo en milisegundos
}

export interface ChatParameters {
  model: string;
  temperature: number;
  context: string;
}
