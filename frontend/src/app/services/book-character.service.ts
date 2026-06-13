import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { ChatMessage, UploadResponse, ChatResponse } from '../models/chat.model';

@Injectable({
  providedIn: 'root'
})
export class BookCharacterService {
  private apiUrl = 'http://127.0.0.1:8000';

  private collectionNameSubject = new BehaviorSubject<string | null>(null);
  private characterNameSubject = new BehaviorSubject<string | null>(null);
  private chatMessagesSubject = new BehaviorSubject<ChatMessage[]>([]);
  private loadingSubject = new BehaviorSubject<boolean>(false);

  collectionName$ = this.collectionNameSubject.asObservable();
  characterName$ = this.characterNameSubject.asObservable();
  chatMessages$ = this.chatMessagesSubject.asObservable();
  loading$ = this.loadingSubject.asObservable();

  constructor(private http: HttpClient) {}

  uploadPDF(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<UploadResponse>(`${this.apiUrl}/upload`, formData);
  }

 sendMessage(query: string): Observable<ChatResponse> {
  const collection = this.collectionNameSubject.value;
  const character = this.characterNameSubject.value;
  const messages = this.chatMessagesSubject.value;

  if (!collection || !character) {
    throw new Error('Collection name and character name are required');
  }

  // Build conversation history
  const history = messages.map(m => ({
    role: m.role === 'user' ? 'user' : 'assistant',
    content: m.content
  }));

  return this.http.post<ChatResponse>(
    `${this.apiUrl}/chat`,
    { history },
    {
      params: {
        query,
        character_name: character,
        collection_name: collection
      }
    }
  );
}

  setCollectionName(name: string): void {
    this.collectionNameSubject.next(name);
  }

  setCharacterName(name: string): void {
    this.characterNameSubject.next(name);
  }

  addMessage(message: ChatMessage): void {
    const current = this.chatMessagesSubject.value;
    this.chatMessagesSubject.next([...current, message]);
  }

  clearChat(): void {
    this.chatMessagesSubject.next([]);
  }

  setLoading(loading: boolean): void {
    this.loadingSubject.next(loading);
  }

  startNewChat(characterName: string, collectionName: string): void {
    this.setCharacterName(characterName);
    this.setCollectionName(collectionName);
    this.clearChat();
  }
}
