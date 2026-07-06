# ScoutAI

ScoutAI is an AI-powered client acquisition workspace that helps freelancers, developers, and agencies discover businesses, analyze their online presence, generate personalized outreach, manage conversations, and close more deals. It acts as an intelligent "second brain" for your sales operations.

## Architecture

ScoutAI is a modern monolithic architecture with a decoupled React frontend and a FastAPI backend.

- **Frontend**: React, Vite, TypeScript, Tailwind CSS, TanStack Query, Zustand, React Router
- **Backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, PyJWT, Argon2
- **AI Integration**: Google Gemini AI (via `google-genai` SDK)

### Modules
1. **Scout Engine**: Search and discover businesses intelligently.
2. **AI Business Intelligence**: Automatically analyze websites and determine "Opportunity Scores."
3. **AI Outreach**: Generate highly personalized emails and messages avoiding generic AI tones.
4. **CRM & Conversation Intelligence**: Kanban pipeline with automated sentiment and buying intent analysis.
5. **AI Copilot**: A global AI assistant that understands your entire workspace context.
6. **Proposal & Document Engine**: Pre-filled Markdown documents built on business data.
7. **Analytics**: Funnel tracking, revenue, and actionable AI insights.

## Development Setup

### Prerequisites
- Node.js (v20+)
- Python (3.11+)
- PostgreSQL (15+)
- Gemini API Key

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MongoDB Atlas URI and GEMINI_API_KEY

uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env and point VITE_API_URL to your backend

npm run dev
```

## Production Deployment

ScoutAI is fully containerized for production deployment.

### Docker Compose
To run everything together (Database, Backend, Frontend) via Docker Compose:
```bash
docker-compose up --build -d
```

### Manual Deployment
- **Frontend**: Designed to be deployed on platforms like **Vercel** or **Netlify**. Ensure environment variables are set.
- **Backend**: Can be deployed on **Render**, **Railway**, or **AWS/GCP/DigitalOcean** using the provided `Dockerfile`.
- **Database**: Use a managed PostgreSQL provider such as **Supabase**, **Neon**, or **AWS RDS**.

## Security Features
- **Argon2 Password Hashing**: Modern, highly secure hashing.
- **JWT Rotation**: Access tokens with strict expiration.
- **CORS Protection**: Configured via FastAPI middleware.
- **Security Headers**: Content-Security-Policy, X-Frame-Options, X-XSS-Protection handled automatically.
- **Global Error Handling**: Frontend `ErrorBoundary` masks stack traces from users; backend generic 500 error catching.

## Versioning
Current Release: **v1.0.0**

*Built for production scale and maintainability.*
