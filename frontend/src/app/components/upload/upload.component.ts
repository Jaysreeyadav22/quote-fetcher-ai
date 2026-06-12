import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookCharacterService } from '../../services/book-character.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  @Output() uploadComplete = new EventEmitter<{ characterName: string; collectionName: string }>();

  fileName: string | null = null;
  characterName = '';
  loading$ = this.bookCharacterService.loading$;
  errorMessage = '';
  selectedFile: File | null = null;

  constructor(private bookCharacterService: BookCharacterService) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.fileName = this.selectedFile.name;
      this.errorMessage = '';
    }
  }

  onSubmit(): void {
    if (!this.selectedFile || !this.characterName.trim()) {
      this.errorMessage = 'Please select a file and enter a character name.';
      return;
    }

    this.bookCharacterService.setLoading(true);
    this.bookCharacterService.uploadPDF(this.selectedFile).subscribe({
      next: (response) => {
        this.bookCharacterService.setLoading(false);
        this.uploadComplete.emit({
          characterName: this.characterName.trim(),
          collectionName: response.collection_name
        });
      },
      error: (error) => {
        this.bookCharacterService.setLoading(false);
        this.errorMessage = error.error?.error || 'Upload failed. Please try again.';
        console.error('Upload error:', error);
      }
    });
  }
}
