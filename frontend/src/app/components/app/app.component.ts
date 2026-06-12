import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { UploadComponent } from '../upload/upload.component';
import { ChatComponent } from '../chat/chat.component';
import { BookCharacterService } from '../../services/book-character.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule, UploadComponent, ChatComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  characterName$ = this.bookCharacterService.characterName$;

  constructor(private bookCharacterService: BookCharacterService) {}

  onUploadComplete(event: { characterName: string; collectionName: string }): void {
    this.bookCharacterService.startNewChat(event.characterName, event.collectionName);
  }
}
