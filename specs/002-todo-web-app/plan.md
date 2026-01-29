# Implementation Plan: Full-Stack Multi-User Web Todo Application

**Branch**: `002-todo-web-app` | **Date**: 2026-01-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-web-app/spec.md`

**Note**: This document outlines the architectural design and technical approach for Phase II.

## Summary

Transform the Phase I CLI Todo application into a full-stack, multi-user web application with secure authentication and user data isolation. The system uses a monorepo architecture with Next.js 16+ frontend and FastAPI backend, JWT-based authentication via Better Auth, and Neon Serverless PostgreSQL for data persistence. Each user can create, read, update, and delete their own tasks with complete data isolation enforced at both API and database levels.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5+, JavaScript (ES2023)
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16+ (App Router), React 19+, Tailwind CSS, Better Auth client
- Backend: FastAPI 0.115+, SQLModel 0.0.22+, Better Auth, Pydantic 2+, Alembic
- Database: Neon Serverless PostgreSQL

**Storage**: Neon Serverless PostgreSQL with SQLModel ORM

**Testing**:
- Frontend: React Testing Library, Jest
- Backend: pytest with async support
- Contract: OpenAPI schema validation

**Target Platform**: Web (cross-browser), deployed on Vercel (frontend) + cloud hosting (backend)

**Project Type**: Web application (monorepo with separate frontend and backend)

**Performance Goals**:
- API response time: p95 < 500ms, p99 < 1s
- Frontend initial load: < 2 seconds
- Task operations complete: < 1 second with visual feedback
- Support 100+ concurrent users

**Constraints**:
- Stateless authentication (JWT) for horizontal scalability
- HTTPS required in production
- User data isolation enforced at every layer
- No cross-user data access permitted
- Frontend bundle < 500KB initial load

**Scale/Scope**:
- Support up to 100,000 users
- Handle up to 1,000,000 tasks
- Average 1000 tasks per active user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development First ✅
- **Status**: PASS
- **Compliance**: All design decisions traced to spec.md requirements
- **Evidence**: Specification complete with 37 functional requirements and 4 prioritized user stories

### Principle II: Full-Stack Code Quality Standard ✅
- **Status**: PASS
- **Backend**: Python 3.13+ with PEP 8, type hints, docstrings, FastAPI best practices
- **Frontend**: TypeScript strict mode, Next.js 16+ App Router, ESLint/Prettier
- **Verification**: Linting and type checking configured in quality gates

### Principle III: TDD Mandatory ✅
- **Status**: PASS
- **Backend**: pytest framework with contract, integration, and unit tests
- **Frontend**: React Testing Library for component tests
- **Process**: Red-Green-Refactor cycle enforced in tasks phase

### Principle IV: PostgreSQL Database Standard ✅
- **Status**: PASS
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel with Alembic migrations
- **Constraints**: Foreign keys, indexes, timestamps required on all tables

### Principle V: API & Frontend Standards ✅
- **Status**: PASS
- **API**: RESTful design, `/api/v1/` versioning, OpenAPI documentation
- **Frontend**: Next.js App Router, Server Components default, error boundaries
- **HTTP**: Proper status codes (200, 201, 400, 401, 403, 404, 500)

### Principle VI: Measurable Acceptance Criteria ✅
- **Status**: PASS
- **Spec Quality**: 10 measurable success criteria defined
- **Format**: Given-When-Then scenarios for all user stories
- **Coverage**: 20 acceptance scenarios across 4 user stories

### Principle VII: Monorepo Architecture Mandate ✅
- **Status**: PASS
- **Structure**: Turborepo + pnpm workspaces
- **Organization**: `apps/web/` (Next.js) + `apps/api/` (FastAPI)
- **Shared**: `packages/types/` for API contracts

### Principle VIII: JWT Authentication & User Isolation ✅
- **Status**: PASS
- **Auth**: Better Auth with JWT (15min access, 7-day refresh tokens)
- **Isolation**: user_id foreign key on all tasks, ownership validation required
- **Security**: bcrypt hashing, token rotation, logout invalidation

### Principle IX: Security & Error Handling ✅
- **Status**: PASS
- **Input Validation**: Frontend + backend validation required
- **SQL Injection**: Prevented via SQLModel ORM
- **XSS**: Prevented via React automatic escaping
- **Error Format**: Structured JSON with user-friendly messages

**Gate Result**: ✅ **PASS** - All constitutional principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-web-app/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file - implementation plan
├── research.md          # Phase 0 - technology research and decisions
├── data-model.md        # Phase 1 - database schema and entities
├── quickstart.md        # Phase 1 - local development guide
├── contracts/           # Phase 1 - API contracts (OpenAPI specs)
│   ├── auth.yaml        # Authentication endpoints
│   └── tasks.yaml       # Task management endpoints
└── tasks.md             # Phase 2 - executable task list (/sp.tasks)
```

### Source Code (repository root - Monorepo Structure)

```text
todo-app/
├── .specify/
│   ├── memory/
│   │   └── constitution.md        # Phase II constitution v2.0.0
│   ├── templates/                 # SpecKit Plus templates
│   └── scripts/                   # Automation scripts
│
├── apps/
│   ├── web/                       # Next.js 16+ frontend
│   │   ├── src/
│   │   │   ├── app/               # App Router (Pages & Layouts)
│   │   │   │   ├── (auth)/        # Auth route group
│   │   │   │   │   ├── login/
│   │   │   │   │   └── signup/
│   │   │   │   ├── (dashboard)/   # Protected route group
│   │   │   │   │   ├── tasks/
│   │   │   │   │   └── layout.tsx # Auth wrapper
│   │   │   │   ├── layout.tsx     # Root layout
│   │   │   │   └── page.tsx       # Landing page
│   │   │   ├── components/        # React components
│   │   │   │   ├── auth/          # Login/Signup forms
│   │   │   │   ├── tasks/         # Task list, task card, task form
│   │   │   │   ├── ui/            # Shared UI components
│   │   │   │   └── providers/     # Context providers
│   │   │   ├── lib/               # Utilities and helpers
│   │   │   │   ├── api-client.ts  # API communication
│   │   │   │   ├── auth.ts        # Auth utilities
│   │   │   │   └── validation.ts  # Form validation
│   │   │   ├── hooks/             # Custom React hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   └── useTasks.ts
│   │   │   └── types/             # TypeScript types
│   │   │       └── index.ts
│   │   ├── public/                # Static assets
│   │   ├── tests/                 # Frontend tests
│   │   │   ├── components/        # Component tests
│   │   │   └── integration/       # Integration tests
│   │   ├── .env.local.example     # Environment template
│   │   ├── next.config.js         # Next.js configuration
│   │   ├── tailwind.config.js     # Tailwind configuration
│   │   ├── tsconfig.json          # TypeScript configuration
│   │   └── package.json
│   │
│   └── api/                       # FastAPI backend
│       ├── src/
│       │   ├── models/            # SQLModel entities
│       │   │   ├── __init__.py
│       │   │   ├── user.py        # User model
│       │   │   └── task.py        # Task model
│       │   ├── schemas/           # Pydantic request/response schemas
│       │   │   ├── __init__.py
│       │   │   ├── auth.py        # Auth DTOs
│       │   │   └── task.py        # Task DTOs
│       │   ├── routers/           # API endpoints
│       │   │   ├── __init__.py
│       │   │   ├── auth.py        # Auth routes
│       │   │   └── tasks.py       # Task routes
│       │   ├── services/          # Business logic
│       │   │   ├── __init__.py
│       │   │   ├── auth_service.py
│       │   │   └── task_service.py
│       │   ├── auth/              # Authentication
│       │   │   ├── __init__.py
│       │   │   ├── jwt.py         # JWT utilities
│       │   │   ├── password.py    # Password hashing
│       │   │   └── dependencies.py # FastAPI dependencies
│       │   ├── core/              # Core configuration
│       │   │   ├── __init__.py
│       │   │   ├── config.py      # Settings (Pydantic BaseSettings)
│       │   │   └── security.py    # Security utilities
│       │   ├── database.py        # Database connection
│       │   └── main.py            # FastAPI application
│       ├── tests/                 # Backend tests
│       │   ├── __init__.py
│       │   ├── conftest.py        # Pytest fixtures
│       │   ├── contract/          # API contract tests
│       │   │   ├── test_auth_api.py
│       │   │   └── test_tasks_api.py
│       │   ├── integration/       # Integration tests
│       │   │   └── test_user_isolation.py
│       │   └── unit/              # Unit tests
│       │       ├── test_auth_service.py
│       │       └── test_task_service.py
│       ├── alembic/               # Database migrations
│       │   ├── versions/          # Migration scripts
│       │   ├── env.py             # Alembic configuration
│       │   └── alembic.ini
│       ├── .env.example           # Environment template
│       ├── pyproject.toml         # Python dependencies
│       └── README.md
│
├── packages/
│   ├── types/                     # Shared TypeScript types
│   │   ├── api-types.ts           # API contract types
│   │   └── package.json
│   └── config/                    # Shared configurations
│       ├── eslint-config/
│       │   └── package.json
│       └── typescript-config/
│           ├── base.json
│           └── package.json
│
├── specs/                         # Feature specifications
│   ├── 001-todo-console-app/      # Phase I (archived)
│   └── 002-todo-web-app/          # Phase II (current)
│
├── history/
│   ├── prompts/                   # Prompt History Records
│   │   ├── constitution/
│   │   ├── todo-web-app/
│   │   └── general/
│   └── adr/                       # Architecture Decision Records
│
├── .gitignore                     # Git ignore patterns
├── turbo.json                     # Turborepo configuration
├── pnpm-workspace.yaml            # pnpm workspaces
├── package.json                   # Root dependencies & scripts
└── README.md                      # Project overview
```

**Structure Decision**: Selected **Web Application (Monorepo)** structure per Principle VII. The monorepo uses:
- **apps/web/**: Next.js 16+ frontend with App Router structure
- **apps/api/**: FastAPI backend with clean architecture
- **packages/**: Shared code (types, configs) for code reuse
- **Turborepo**: For task orchestration, caching, and parallel execution
- **pnpm workspaces**: For efficient package management

This structure satisfies constitutional requirements for monorepo architecture and enables independent deployment while maintaining code cohesion.

## Complexity Tracking

> **No violations** - All constitutional principles are satisfied. No justification needed.

---

## Architecture Overview

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          Next.js 16+ Frontend (apps/web)                    │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │  Auth Pages  │  │  Task Pages  │  │   UI Components  │ │ │
│  │  │ (login/signup)  │  (dashboard)  │  │ (forms, lists)   │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  │                                                              │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │      Client-Side State (JWT tokens, user context)    │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTPS (JSON + JWT)
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (apps/api)                     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   API Routers (/api/v1/)                  │   │
│  │  ┌──────────────────┐        ┌───────────────────────┐   │   │
│  │  │  /auth/register  │        │  /tasks (CRUD)        │   │   │
│  │  │  /auth/login     │        │  - GET    (list)      │   │   │
│  │  │  /auth/refresh   │        │  - POST   (create)    │   │   │
│  │  │  /auth/logout    │        │  - GET/:id (retrieve) │   │   │
│  │  └──────────────────┘        │  - PUT/:id (update)   │   │   │
│  │                              │  - DELETE/:id         │   │   │
│  │                              └───────────────────────┘   │   │
│  └────────────────┬──────────────────────┬──────────────────┘   │
│                   │                      │                       │
│  ┌────────────────▼──────┐   ┌──────────▼────────────────┐     │
│  │  Auth Middleware      │   │   Business Services        │     │
│  │  - JWT validation     │   │   - AuthService            │     │
│  │  - User extraction    │   │   - TaskService            │     │
│  │  - 401/403 handling   │   │   - Ownership validation   │     │
│  └────────────────┬──────┘   └──────────┬────────────────┘     │
│                   │                      │                       │
│                   └──────────┬───────────┘                       │
│                              │                                   │
│                   ┌──────────▼────────────────┐                 │
│                   │   SQLModel ORM Layer      │                 │
│                   │   - User model            │                 │
│                   │   - Task model            │                 │
│                   │   - Relationships         │                 │
│                   └──────────┬────────────────┘                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │ SQL queries
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              Neon Serverless PostgreSQL Database                 │
│                                                                   │
│  ┌──────────────────┐           ┌──────────────────────────┐    │
│  │   users table    │           │     tasks table          │    │
│  │  - id (PK)       │           │  - id (PK)               │    │
│  │  - email (UNIQUE)│ ◄─────────│  - user_id (FK, INDEX)   │    │
│  │  - hashed_password          │  - title                 │    │
│  │  - name          │           │  - description           │    │
│  │  - created_at    │           │  - completed             │    │
│  │  - updated_at    │           │  - priority              │    │
│  └──────────────────┘           │  - due_date              │    │
│                                 │  - created_at            │    │
│                                 │  - updated_at            │    │
│                                 └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### Frontend (Next.js 16+ - apps/web/)

**Responsibilities**:
1. **User Interface Rendering**
   - Server Components for initial page load (SEO, performance)
   - Client Components for interactive elements (forms, state)
   - Responsive design (desktop, tablet, mobile >= 375px)

2. **Authentication State Management**
   - Store JWT tokens (localStorage or httpOnly cookies)
   - Automatic token refresh on expiry
   - Redirect to login on 401 responses
   - Provide auth context to components

3. **Form Handling & Validation**
   - Client-side validation before API calls
   - Display inline error messages
   - Loading states during async operations
   - Optimistic UI updates where appropriate

4. **API Communication**
   - HTTP client (fetch or axios) with JWT headers
   - Error handling and user-friendly messages
   - Request/response type safety (TypeScript)

5. **User Experience**
   - Loading skeletons and spinners
   - Error boundaries for graceful failures
   - Toast notifications for success/error feedback
   - Empty states ("No tasks yet")

**Does NOT**:
- ❌ Store passwords or sensitive data
- ❌ Implement business logic (delegate to backend)
- ❌ Validate user ownership (backend responsibility)
- ❌ Direct database access

#### Backend (FastAPI - apps/api/)

**Responsibilities**:
1. **Authentication & Authorization**
   - User registration with password hashing (bcrypt/Argon2)
   - Login with JWT token issuance
   - Token validation middleware
   - Refresh token rotation
   - Logout (token invalidation)

2. **Business Logic**
   - Task CRUD operations
   - User ownership validation
   - Input validation (Pydantic schemas)
   - Business rules enforcement

3. **Data Access & Persistence**
   - Database queries via SQLModel ORM
   - User data isolation (filter by user_id)
   - Transaction management
   - Connection pooling

4. **API Contract**
   - RESTful endpoint implementation
   - OpenAPI documentation generation
   - Proper HTTP status codes
   - Structured error responses

5. **Security**
   - SQL injection prevention (ORM)
   - Input sanitization
   - Rate limiting (auth endpoints)
   - CORS configuration
   - Secrets management (environment variables)

**Does NOT**:
- ❌ Render HTML (API only, no templates)
- ❌ Store plaintext passwords
- ❌ Allow cross-user data access
- ❌ Expose sensitive error details to clients

### Authentication Flow (Better Auth + JWT)

```
Registration Flow:
1. User submits email, name, password (Frontend)
2. POST /api/v1/auth/register (Backend)
3. Validate email uniqueness
4. Hash password with bcrypt
5. Create user record in database
6. Generate JWT access + refresh tokens
7. Return tokens to frontend
8. Store tokens in browser (localStorage/cookie)
9. Redirect to dashboard

Login Flow:
1. User submits email, password (Frontend)
2. POST /api/v1/auth/login (Backend)
3. Find user by email
4. Verify password hash
5. Generate JWT tokens (access: 15min, refresh: 7 days)
6. Return tokens
7. Store tokens in browser
8. Redirect to dashboard

Protected Request Flow:
1. User performs action requiring auth (Frontend)
2. Attach Authorization: Bearer <access_token> header
3. Backend middleware validates JWT signature & expiry
4. Extract user_id from token payload
5. Pass user_id to route handler
6. Service layer filters data by user_id
7. Return response

Token Refresh Flow:
1. Access token expires (15min)
2. API returns 401 Unauthorized
3. Frontend intercepts 401
4. POST /api/v1/auth/refresh with refresh_token
5. Backend validates refresh token
6. Generate new access token
7. Return new access token
8. Retry original request with new token

Logout Flow:
1. User clicks logout (Frontend)
2. POST /api/v1/auth/logout
3. Backend invalidates refresh token (blacklist or DB update)
4. Frontend clears stored tokens
5. Redirect to login page
```

### API Request/Response Lifecycle

```
Example: Create Task

1. User fills task form (Frontend)
   ├─ Title: "Buy groceries"
   ├─ Description: "Milk, eggs, bread"
   └─ Priority: "high"

2. Frontend validation
   ├─ Title not empty ✅
   ├─ Title length <= 200 chars ✅
   └─ Priority in [low, medium, high] ✅

3. POST /api/v1/tasks
   Headers:
     Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   Body:
     {
       "title": "Buy groceries",
       "description": "Milk, eggs, bread",
       "priority": "high"
     }

4. Backend Middleware
   ├─ Extract JWT from Authorization header
   ├─ Validate signature & expiry
   ├─ Extract user_id from payload → user_id=42
   └─ Pass to route handler via dependency injection

5. Route Handler (routers/tasks.py)
   ├─ Validate request body with Pydantic schema
   └─ Call TaskService.create_task(user_id=42, data=...)

6. Service Layer (services/task_service.py)
   ├─ Create Task model with user_id=42
   ├─ Auto-generate: id, created_at, updated_at
   └─ Save to database via SQLModel

7. Database Query
   INSERT INTO tasks (user_id, title, description, priority, completed, created_at, updated_at)
   VALUES (42, 'Buy groceries', 'Milk, eggs, bread', 'high', false, NOW(), NOW())
   RETURNING *;

8. Backend Response (201 Created)
   {
     "id": 123,
     "user_id": 42,
     "title": "Buy groceries",
     "description": "Milk, eggs, bread",
     "priority": "high",
     "completed": false,
     "due_date": null,
     "created_at": "2026-01-05T14:30:00Z",
     "updated_at": "2026-01-05T14:30:00Z"
   }

9. Frontend Updates
   ├─ Add task to local state (optimistic update)
   ├─ Display success toast
   └─ Clear form inputs
```

### Database Schema Overview

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    completed BOOLEAN DEFAULT false,
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high')),
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);

-- Constraints ensure data isolation
-- All task queries MUST filter by user_id
-- Foreign key cascade ensures cleanup on user deletion
```

**Key Design Decisions**:
1. **user_id foreign key**: Enforces referential integrity
2. **CASCADE delete**: Removing user deletes all their tasks
3. **Indexes**: Optimize queries on user_id, completed, due_date
4. **Timestamps**: Track creation and modification times
5. **Priority enum**: Constrained to valid values at DB level

### Environment Variable Strategy

#### Frontend (.env.local)
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Authentication
NEXT_PUBLIC_TOKEN_STORAGE=localStorage  # or 'cookie'

# Feature Flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
# For Neon: postgresql://user:password@ep-xyz.neon.tech/todo_db?sslmode=require

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-min-32-chars-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
PASSWORD_HASH_ROUNDS=12

# Application
ENVIRONMENT=development  # development, staging, production
DEBUG=true
```

**Security Notes**:
- ❌ Never commit .env files to git
- ✅ Provide .env.example templates
- ✅ Use environment-specific values
- ✅ Rotate JWT secrets regularly in production
- ✅ Use strong, randomly generated secrets

### Deployment Strategy

#### Frontend Deployment (Vercel)

**Platform**: Vercel (recommended for Next.js)

**Configuration**:
- **Build Command**: `pnpm turbo build --filter=web`
- **Output Directory**: `apps/web/.next`
- **Environment Variables**: Set in Vercel dashboard
- **Domains**: Auto-SSL via Vercel

**Advantages**:
- Optimized for Next.js (Edge Runtime, ISR, Streaming)
- Automatic HTTPS
- Global CDN
- Preview deployments for PRs
- Zero-config deployment

#### Backend Deployment (Cloud Hosting)

**Options**:
1. **Railway / Render** (Recommended for MVP)
   - Docker container deployment
   - Automatic HTTPS
   - Environment variable management
   - Neon PostgreSQL integration

2. **AWS ECS / Google Cloud Run**
   - Production-grade scalability
   - Container orchestration
   - Auto-scaling based on load

3. **DigitalOcean App Platform**
   - Simplified PaaS
   - Managed databases
   - Automatic deployments from Git

**Deployment Steps**:
1. **Containerize Backend**
   ```dockerfile
   FROM python:3.13-slim
   WORKDIR /app
   COPY pyproject.toml ./
   RUN pip install poetry && poetry install --no-dev
   COPY src ./src
   CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Configure Environment**
   - Set DATABASE_URL (Neon connection string)
   - Set JWT_SECRET_KEY (strong random value)
   - Set CORS_ORIGINS (frontend URL)

3. **Run Migrations**
   - `alembic upgrade head` on deployment

4. **Health Checks**
   - Endpoint: `GET /health` → 200 OK
   - Monitor uptime and response times

#### Database (Neon PostgreSQL)

**Setup**:
1. Create Neon project at https://neon.tech
2. Create database: `todo_production`
3. Copy connection string
4. Configure in backend environment

**Advantages**:
- Serverless scaling (auto-pause when idle)
- Automatic backups
- Branching for development/staging
- Sub-100ms query latency
- Built-in connection pooling

---

## Next Steps

This implementation plan is now complete. Proceed to:

1. **Phase 0**: Run research phase to generate `research.md`
2. **Phase 1**: Generate `data-model.md`, `contracts/`, and `quickstart.md`
3. **Phase 2**: Run `/sp.tasks` to create executable task list
4. **Implement**: Execute tasks using Red-Green-Refactor cycle

**Ready for Phase 0 Research**: ✅
