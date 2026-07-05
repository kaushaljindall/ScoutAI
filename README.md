# ScoutAI

ScoutAI is a premium, AI-powered workspace designed for freelancers, agencies, and developers to discover potential clients, analyze their online presence, generate personalized outreach messages, manage conversations, and track follow-ups in one place.

## Architecture

This project is structured as a monorepo containing two independently deployable applications:

- **`frontend/`**: The React UI built with Vite, TypeScript, and Tailwind CSS.
- **`backend/`**: The RESTful API built with FastAPI, SQLAlchemy, and Alembic.

Both applications communicate via REST APIs and are configured to be entirely decoupled.

---

## Tech Stack

### Frontend
- **Framework**: React (Vite)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **State Management**: Zustand (UI state) & TanStack Query (Server state)
- **Routing**: React Router
- **Form Handling**: React Hook Form with Zod validation
- **Animations**: Framer Motion
- **HTTP Client**: Axios (with JWT interceptors)
- **UI Components**: Custom `shadcn/ui`-inspired components (`tailwind-merge`, `clsx`)

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT & Argon2 Password Hashing
- **Validation**: Pydantic & Pydantic-Settings

---

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.11+
- PostgreSQL (or a Supabase project)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: ensure you install `fastapi uvicorn sqlalchemy alembic psycopg2-binary passlib[argon2] python-jose[cryptography] pydantic pydantic-settings python-multipart python-dotenv email-validator` if requirements.txt is not present yet)*
4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Run database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

---

## Deployment Target

- **Frontend**: Designed to be deployed on **Vercel**.
- **Backend**: Designed to be deployed on **Render**.
- **Database**: Hosted on **Supabase PostgreSQL**.

*(Note: The frontend must **never** communicate directly with Supabase. All database operations happen securely via the FastAPI backend.)*

---

## Current Features (Foundation Phase)
- ✅ Scalable folder structure for both Frontend and Backend
- ✅ JWT Authentication with Refresh Tokens
- ✅ Protected React Routes
- ✅ Centralized API Service (Axios interceptors)
- ✅ Custom Theme & Reusable UI Components
- ✅ Database Connection & Alembic Migrations Configuration
- ✅ Production-Ready Architectural Setup
