import { Component, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookCharacterService } from '../../services/book-character.service';
import { ChatMessage } from '../../models/chat.model';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  characterName$ = this.bookCharacterService.characterName$;
  messages$ = this.bookCharacterService.chatMessages$;
  loading$ = this.bookCharacterService.loading$;

  userMessage = '';
  errorMessage = '';
  private shouldScroll = false;

  constructor(private bookCharacterService: BookCharacterService) {}

  ngOnInit(): void {}

  ngAfterViewChecked(): void {
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  onSendMessage(): void {
    if (!this.userMessage.trim()) {
      return;
    }

    const query = this.userMessage.trim();
    this.userMessage = '';
    this.errorMessage = '';

    // Add user message to chat
    this.bookCharacterService.addMessage({
      role: 'user',
      content: query,
      timestamp: new Date()
    });

    this.shouldScroll = true;

    // Send message to API
    this.bookCharacterService.setLoading(true);
    this.bookCharacterService.sendMessage(query).subscribe({
      next: (response) => {
        this.bookCharacterService.setLoading(false);
        this.bookCharacterService.addMessage({
          role: 'character',
          content: response.response,
          timestamp: new Date()
        });
        this.shouldScroll = true;
      },
      error: (error) => {
        this.bookCharacterService.setLoading(false);
        this.errorMessage = error.error?.error || 'Failed to get response. Please try again.';
        console.error('Chat error:', error);
      }
    });
  }

 onReset(): void {
  this.bookCharacterService.clearChat();
  this.userMessage = '';
  this.errorMessage = '';
}

onChangeBook(): void {
  this.bookCharacterService.setCharacterName(null as any);
  this.bookCharacterService.setCollectionName(null as any);
  this.bookCharacterService.clearChat();
  this.userMessage = '';
  this.errorMessage = '';
}

  formatTime(date: Date): string {
    return new Date(date).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  private scrollToBottom(): void {
    try {
      this.messagesContainer.nativeElement.scrollTop =
        this.messagesContainer.nativeElement.scrollHeight;
    } catch (error) {
      console.error('Scroll error:', error);
    }
  }
}
