export interface ChatMessage {
  role: 'user' | 'character';
  content: string;
  timestamp: Date;
}

export interface UploadResponse {
  message: string;
  collection_name: string;
}

export interface ChatResponse {
  response: string;
}
