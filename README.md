# StadiumSense AI 🏟️

> GenAI-powered stadium assistant for FIFA World Cup visitors — built with React, Spring Boot, and Gemini AI, deployable on Google Cloud Run.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Google Cloud Run                         │
│                                                                 │
│  ┌─────────────────────┐        ┌──────────────────────────┐   │
│  │   Frontend Service  │        │    Backend Service        │   │
│  │   React + Tailwind  │──────▶ │   Spring Boot (Java 17)  │   │
│  │   served via nginx  │  REST  │   POST /chat             │   │
│  │   (Cloud Run URL)   │        │   GET  /faq              │   │
│  └─────────────────────┘        │   GET  /locations        │   │
│                                 │   GET  /routes           │   │
│                                 │   GET  /health           │   │
│                                 └──────────┬───────────────┘   │
│                                            │                   │
│                                  ┌─────────▼──────────┐        │
│                                  │   Gemini API        │        │
│                                  │ gemini-1.5-flash    │        │
│                                  └─────────────────────┘        │
│                                            │                   │
│                                  ┌─────────▼──────────┐        │
│                                  │  Cloud SQL          │        │
│                                  │  PostgreSQL 16      │        │
│                                  │  (Flyway migrations)│        │
│                                  └─────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘

Local Dev (docker-compose):
  frontend → localhost:3000
  backend  → localhost:8080
  postgres → localhost:5432
```

---

## Local Development

### Prerequisites
- Docker & Docker Compose
- A Gemini API key → [Get one here](https://aistudio.google.com/app/apikey)

### 1. Clone & configure

```bash
git clone https://github.com/aprajitakashyap/MatchFlowAI.git
cd MatchFlowAI
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```

### 2. Start everything

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Health check: http://localhost:8080/health

### 3. Stop

```bash
docker-compose down
# To also remove the DB volume:
docker-compose down -v
```

---

## Project Structure

```
MatchFlowAI/
├── backend/                        # Spring Boot (Java 17)
│   ├── src/main/java/com/stadiumsense/ai/
│   │   ├── controller/             # REST controllers
│   │   ├── service/                # ChatService, GeminiService, ContextService
│   │   ├── model/                  # JPA entities
│   │   ├── repository/             # Spring Data repos
│   │   ├── dto/                    # Request/Response records
│   │   └── config/                 # CORS config
│   ├── src/main/resources/
│   │   ├── db/migration/           # Flyway SQL (schema + seed data)
│   │   └── application.properties
│   ├── Dockerfile                  # Multi-stage, non-root
│   └── pom.xml
├── frontend/                       # React + Tailwind (Vite)
│   ├── src/
│   │   ├── components/             # ChatWindow, MessageBubble, ChatInput, etc.
│   │   ├── hooks/useChat.js        # Chat state management
│   │   ├── utils/api.js            # Backend API calls
│   │   └── App.jsx
│   ├── nginx.conf                  # SPA routing + health endpoint
│   ├── Dockerfile                  # Multi-stage, non-root
│   └── package.json
├── docker-compose.yml              # Local dev: frontend + backend + postgres
├── .env.example                    # Environment variable template
└── README.md
```

---

## Deploy to Google Cloud Run

### Prerequisites

```bash
# Authenticate
gcloud auth login
gcloud auth configure-docker

# Set your project
export PROJECT_ID=your-gcp-project-id
export REGION=us-central1
gcloud config set project $PROJECT_ID
```

### 1. Create Cloud SQL (PostgreSQL)

```bash
gcloud sql instances create stadiumsense-db \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --region=$REGION

gcloud sql databases create stadiumsense --instance=stadiumsense-db
gcloud sql users create stadiumsense --instance=stadiumsense-db --password=YOUR_DB_PASSWORD
```

### 2. Store secrets in Secret Manager

```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=-
echo -n "YOUR_DB_PASSWORD"    | gcloud secrets create DB_PASSWORD     --data-file=-
```

### 3. Build & push Docker images

```bash
# Backend
docker build -t gcr.io/$PROJECT_ID/stadiumsense-backend:latest ./backend
docker push gcr.io/$PROJECT_ID/stadiumsense-backend:latest

# Frontend (backend URL filled in after backend deploy)
docker build \
  --build-arg VITE_BACKEND_URL=https://stadiumsense-backend-HASH-uc.a.run.app \
  -t gcr.io/$PROJECT_ID/stadiumsense-frontend:latest ./frontend
docker push gcr.io/$PROJECT_ID/stadiumsense-frontend:latest
```

### 4. Deploy Backend to Cloud Run

```bash
gcloud run deploy stadiumsense-backend \
  --image=gcr.io/$PROJECT_ID/stadiumsense-backend:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=8080 \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=5 \
  --set-env-vars="DB_URL=jdbc:postgresql:///stadiumsense?cloudSqlInstance=$PROJECT_ID:$REGION:stadiumsense-db&socketFactory=com.google.cloud.sql.postgres.SocketFactory" \
  --set-env-vars="DB_USER=stadiumsense" \
  --set-secrets="DB_PASSWORD=DB_PASSWORD:latest,GEMINI_API_KEY=GEMINI_API_KEY:latest" \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:stadiumsense-db
```

### 5. Deploy Frontend to Cloud Run

```bash
# Get the backend URL from the previous deploy output, then:
export BACKEND_URL=https://stadiumsense-backend-HASH-uc.a.run.app

gcloud run deploy stadiumsense-frontend \
  --image=gcr.io/$PROJECT_ID/stadiumsense-frontend:latest \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated \
  --port=8080 \
  --memory=256Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=5
```

### 6. Set CORS on backend

```bash
export FRONTEND_URL=https://stadiumsense-frontend-HASH-uc.a.run.app

gcloud run services update stadiumsense-backend \
  --region=$REGION \
  --set-env-vars="FRONTEND_URL=$FRONTEND_URL"
```

---

## API Reference

| Method | Endpoint     | Description                              |
|--------|-------------|------------------------------------------|
| POST   | `/chat`      | Send message, get AI response            |
| GET    | `/faq`       | List all FAQs                            |
| GET    | `/locations` | List all stadium locations               |
| GET    | `/routes`    | List all routes (with accessibility flag)|
| GET    | `/health`    | Health check for Cloud Run               |

### POST /chat

```json
// Request
{ "message": "Where is the nearest restroom?", "language": "en" }

// Response
{ "response": "The nearest accessible restroom is at Gate A on Level 1." }
```

Supported languages: `en` (English), `es` (Español), `fr` (Français)

---

## Environment Variables

| Variable        | Service  | Description                        |
|----------------|----------|------------------------------------|
| `GEMINI_API_KEY`| Backend  | Google Gemini API key (required)   |
| `DB_URL`        | Backend  | JDBC connection URL                |
| `DB_USER`       | Backend  | PostgreSQL username                |
| `DB_PASSWORD`   | Backend  | PostgreSQL password                |
| `FRONTEND_URL`  | Backend  | Frontend URL for CORS              |
| `PORT`          | Backend  | Server port (default: 8080)        |
| `VITE_BACKEND_URL` | Frontend | Backend Cloud Run URL (build-time)|
