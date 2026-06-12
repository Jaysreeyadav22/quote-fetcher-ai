# Book Character Chat - Frontend Requirements

## App Overview
A web app where users upload any book (PDF) and have a conversation 
with a character from that book. The AI responds in character, 
grounded in the actual book text.

## User Flow
1. User lands on home screen
2. User uploads a PDF book
3. User enters the character name they want to talk to
4. App processes the upload (show loading state)
5. Chat screen appears
6. User types messages to the character
7. Character responds in their voice based on book content

## API Endpoints
- POST /upload — FormData with PDF file
  - Returns: { message: string, collection_name: string }
- POST /chat — query params: query, character_name, collection_name
  - Returns: { response: string }

## UI Style
- Dark background (#0f0f0f)
- Cream/warm text (#f5e6d3)
- Single page app — upload section top, chat below
- Minimal, literary, elegant feel
- Loading spinner during upload and chat response
- User messages on right, character messages on left
- Character name shown at top of chat like a contact

## Components Needed
- AppComponent — main shell
- UploadComponent — PDF upload + character name input
- ChatComponent — message input + chat bubbles

## Tech
- Angular 17 standalone components
- HttpClient for API calls
- Simple service with BehaviorSubject for state
- SCSS for styling