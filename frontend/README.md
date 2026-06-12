# Book Character Chat - Frontend

Angular 17 standalone components frontend for the Book Character Chat application.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── models/
│   │   │   └── chat.model.ts
│   │   ├── services/
│   │   │   └── book-character.service.ts
│   │   └── components/
│   │       ├── app/
│   │       │   ├── app.component.ts
│   │       │   ├── app.component.html
│   │       │   └── app.component.scss
│   │       ├── upload/
│   │       │   ├── upload.component.ts
│   │       │   ├── upload.component.html
│   │       │   └── upload.component.scss
│   │       └── chat/
│   │           ├── chat.component.ts
│   │           ├── chat.component.html
│   │           └── chat.component.scss
│   ├── main.ts
│   ├── index.html
│   └── styles.scss
├── package.json
├── tsconfig.json
├── angular.json
└── README.md
```

## Setup

### Prerequisites
- Node.js 18+
- npm 9+

### Installation

```bash
cd frontend
npm install
```

### Development Server

```bash
npm start
```

Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

### Build for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Components

### AppComponent
Main shell component that manages the page layout and routing between upload and chat sections.

**Files:**
- `app.component.ts` - Component logic
- `app.component.html` - Template
- `app.component.scss` - Styles

### UploadComponent
Handles PDF file upload and character name input.

**Files:**
- `upload.component.ts` - Component logic
- `upload.component.html` - Template
- `upload.component.scss` - Styles

**Features:**
- PDF file picker
- Character name input
- Loading state
- Error handling

### ChatComponent
Displays conversation with the character and handles message sending.

**Files:**
- `chat.component.ts` - Component logic
- `chat.component.html` - Template
- `chat.component.scss` - Styles

**Features:**
- Message history display
- User and character messages differentiated
- Auto-scroll to latest message
- Typing indicator
- Reset chat button
- Error handling

## Services

### BookCharacterService
Manages application state and API communication using RxJS BehaviorSubjects.

**Methods:**
- `uploadPDF(file)` - Upload PDF to backend
- `sendMessage(query)` - Send chat message
- `setCollectionName(name)` - Set active collection
- `setCharacterName(name)` - Set active character
- `addMessage(message)` - Add message to chat history
- `clearChat()` - Clear chat history
- `startNewChat(characterName, collectionName)` - Initialize new chat session

## Models

### ChatMessage
```typescript
interface ChatMessage {
  role: 'user' | 'character';
  content: string;
  timestamp: Date;
}
```

### UploadResponse
```typescript
interface UploadResponse {
  message: string;
  collection_name: string;
}
```

### ChatResponse
```typescript
interface ChatResponse {
  response: string;
}
```

## Styling

- **Theme Colors:**
  - Background: `#0f0f0f` (dark)
  - Text: `#f5e6d3` (cream/warm)
  - Accents: `#2a2a2a`, `#3a3a3a`
  - User message: `#3a5a4a` (muted green)
  - Character message: `#2a2a2a` (dark gray)

- **Typography:**
  - Primary font: Georgia serif
  - UI font: Segoe UI

## Configuration

### API Endpoint
Update the `apiUrl` in `book-character.service.ts` if your backend is running on a different port:

```typescript
private apiUrl = 'http://127.0.0.1:8000'; // Change if needed
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
