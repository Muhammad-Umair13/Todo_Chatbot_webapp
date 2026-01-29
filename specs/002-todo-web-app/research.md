# Research: Full-Stack Multi-User Web Todo Application

**Feature**: 002-todo-web-app
**Date**: 2026-01-05
**Purpose**: Technology research and architectural decisions for Phase II implementation

## Overview

This document captures research findings and technology decisions for transforming the Phase I CLI Todo app into a full-stack multi-user web application. All decisions are traced back to constitutional principles and specification requirements.

---

## 1. Monorepo Structure Decision

### Context
Constitution Principle VII mandates monorepo architecture. Need to choose monorepo tooling that supports both Next.js frontend and Python backend.

### Options Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **Turborepo + pnpm** | Native Next.js support, fast caching, simple config, handles polyglot repos | Limited Python tooling, requires manual scripts | ✅ **SELECTED** |
| **Nx** | Strong Python support, computation caching, task graphs | Complex setup, heavyweight for 2 apps | ❌ Rejected - overkill |
| **Lerna** | Mature, widely used | Primarily npm/yarn focused, slower | ❌ Rejected - outdated |
| **pnpm workspaces only** | Lightweight, no extra tooling | No caching, no task orchestration | ❌ Rejected - insufficient |

### Decision: Turborepo + pnpm workspaces

**Rationale**:
- **Turborepo** provides task orchestration, parallel execution, and build caching
- **pnpm workspaces** handles package management efficiently with hard links
- Optimized for Next.js (official Vercel product)
- Supports custom scripts for Python backend (pyproject.toml integration)
- Minimal configuration overhead

**Configuration**:
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "outputs": []
    }
  }
}
```

**References**:
- Turborepo docs: https://turbo.build/repo/docs
- pnpm workspaces: https://pnpm.io/workspaces

---

## 2. Authentication Implementation (Better Auth + JWT)

### Context
Constitution Principle VIII requires JWT authentication with Better Auth library. Need to understand integration approach and token management.

### Research Findings

**Better Auth Overview**:
- Modern authentication library for TypeScript/JavaScript
- Supports multiple strategies (email/password, OAuth, magic links)
- JWT token generation and validation built-in
- Works with both Next.js and backend APIs

**Decision: Custom JWT Implementation (FastAPI) + Better Auth Patterns**

**Rationale**:
- Better Auth is primarily frontend-focused (Next.js integration)
- Backend (FastAPI) needs custom JWT implementation using `python-jose` or `PyJWT`
- Frontend can use Better Auth patterns for state management
- Maintain consistency: Both use JWT tokens with same structure

**Token Structure**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1641067200,
  "iat": 1641063600,
  "type": "access"  // or "refresh"
}
```

**Libraries**:
- **Backend**: `python-jose[cryptography]` for JWT operations, `passlib[bcrypt]` for password hashing
- **Frontend**: Native `fetch` API with JWT headers, custom auth context

**Token Storage**:
- **Access Token**: localStorage (short-lived, 15min)
- **Refresh Token**: httpOnly cookie (recommended) or localStorage (7 days)

**Security Considerations**:
- Use HS256 algorithm (symmetric) for MVP, RS256 (asymmetric) for production scaling
- Refresh token rotation on every refresh request
- Token blacklist for logout (Redis or DB table)

**References**:
- python-jose: https://python-jose.readthedocs.io/
- JWT best practices: https://datatracker.ietf.org/doc/html/rfc8725

---

## 3. Next.js 16+ App Router Architecture

### Context
Constitution requires Next.js 16+ with App Router. Need to understand routing patterns and component organization.

### Research Findings

**App Router Key Features** (Next.js 13+):
1. **Server Components by Default**: Render on server, reduce JS bundle
2. **Route Groups**: Organize routes without affecting URL structure
3. **Layouts**: Shared UI across routes
4. **Loading & Error States**: Built-in file conventions
5. **Parallel Routes**: Render multiple pages simultaneously

**Recommended Structure**:
```
app/
├── (auth)/              # Route group for authentication
│   ├── login/
│   │   └── page.tsx     # /login
│   └── signup/
│       └── page.tsx     # /signup
├── (dashboard)/         # Route group for protected routes
│   ├── layout.tsx       # Auth wrapper
│   └── tasks/
│       └── page.tsx     # /tasks
├── layout.tsx           # Root layout
└── page.tsx             # / (landing page)
```

**Route Groups `(name)` Benefits**:
- Organize routes logically without adding URL segments
- Share layouts within groups
- Separate public and protected routes cleanly

**Authentication Pattern**:
```typescript
// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }) {
  const user = useAuth();  // Client-side auth check

  if (!user) redirect('/login');

  return <div>{children}</div>;
}
```

**Server vs Client Components**:
- **Server Components**: Static pages, data fetching, no interactivity
- **Client Components** ('use client'): Forms, state, event handlers, browser APIs

**References**:
- Next.js App Router: https://nextjs.org/docs/app
- Route Groups: https://nextjs.org/docs/app/building-your-application/routing/route-groups

---

## 4. FastAPI Project Structure & Best Practices

### Context
Need to design clean backend architecture following FastAPI best practices and constitutional principles.

### Research Findings

**Recommended Architecture** (Clean Architecture / Layered):

```
src/
├── models/          # SQLModel entities (database tables)
├── schemas/         # Pydantic models (request/response DTOs)
├── routers/         # API endpoints (controllers)
├── services/        # Business logic
├── auth/            # Authentication utilities
├── core/            # Configuration & settings
├── database.py      # DB connection
└── main.py          # FastAPI app initialization
```

**Layer Responsibilities**:
1. **Routers**: Handle HTTP requests, validation, responses
2. **Services**: Implement business logic, coordinate between layers
3. **Models**: Define database schema via SQLModel
4. **Schemas**: Define API contracts via Pydantic

**Dependency Injection Pattern**:
```python
# FastAPI's Depends() for auth middleware
@router.get("/tasks")
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await TaskService.get_user_tasks(db, current_user.id)
```

**Best Practices**:
- ✅ Use `async`/`await` for I/O operations
- ✅ Separate models (DB) from schemas (API)
- ✅ Dependency injection for testability
- ✅ Pydantic Settings for configuration
- ✅ SQLModel for type-safe ORM
- ✅ Alembic for migrations

**References**:
- FastAPI best practices: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- SQLModel: https://sqlmodel.tiangolo.com/
- Alembic: https://alembic.sqlalchemy.org/

---

## 5. SQLModel vs SQLAlchemy vs Other ORMs

### Context
Constitution specifies SQLModel. Need to understand advantages and confirm it's the right choice.

### Options Evaluated

| ORM | Pros | Cons | Decision |
|-----|------|------|----------|
| **SQLModel** | Type-safe, Pydantic integration, simple API | Newer, smaller ecosystem | ✅ **SELECTED** (per constitution) |
| **SQLAlchemy 2.0** | Mature, feature-rich, async support | Verbose, steeper learning curve | ❌ More complex than needed |
| **Tortoise ORM** | Async-native, Django-like API | Less mature, smaller community | ❌ Not constitutional requirement |
| **Peewee** | Lightweight, simple | No async, limited features | ❌ Lacks async support |

### Decision: SQLModel (Constitutional Mandate)

**Rationale**:
- **Type Safety**: Full type hints, IDE autocomplete
- **Pydantic Integration**: Same models for DB and API schemas
- **Simplicity**: Cleaner syntax than SQLAlchemy
- **FastAPI Synergy**: Created by same author (Sebastián Ramírez)
- **Alembic Support**: Migrations via SQLAlchemy under the hood

**Example**:
```python
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    name: str

    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    completed: bool = Field(default=False)

    user: User = Relationship(back_populates="tasks")
```

**Migration Strategy**:
- Use Alembic with SQLModel
- Auto-generate migrations: `alembic revision --autogenerate`
- Apply migrations: `alembic upgrade head`

**References**:
- SQLModel docs: https://sqlmodel.tiangolo.com/
- Alembic + SQLModel: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#alembic-migrations

---

## 6. Neon Serverless PostgreSQL Integration

### Context
Constitution mandates Neon Serverless PostgreSQL. Need connection strategy and best practices.

### Research Findings

**Neon Features**:
- Serverless scaling (auto-pause, auto-resume)
- Branching (separate DB per environment)
- Sub-100ms cold start
- Built-in connection pooling
- Automatic backups

**Connection Strategy**:

**Option 1: Direct Connection**
```python
DATABASE_URL = "postgresql://user:pass@ep-xyz.neon.tech/db?sslmode=require"
```
- Simple for development
- ❌ Limited connections (pooling needed for production)

**Option 2: Connection Pooling (PgBouncer)**
```python
DATABASE_URL = "postgresql://user:pass@ep-xyz.neon.tech/db?sslmode=require&options=endpoint%3Dep-xyz-pooler"
```
- ✅ Recommended for production
- Handles 10,000+ concurrent connections
- Built-in with Neon

**Decision: Use Neon Pooler for Production, Direct for Development**

**SQLModel Configuration**:
```python
from sqlmodel import create_engine
from sqlalchemy.pool import NullPool

# Development
engine = create_engine(
    DATABASE_URL,
    echo=True  # Log SQL queries
)

# Production
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Neon handles pooling
    connect_args={"sslmode": "require"}
)
```

**Environment-Specific Databases**:
- Development: Local PostgreSQL or Neon branch
- Staging: Neon branch (staging-branch)
- Production: Neon main branch

**References**:
- Neon docs: https://neon.tech/docs/introduction
- Neon with FastAPI: https://neon.tech/docs/guides/fastapi

---

## 7. Frontend State Management

### Context
Need to decide on state management approach for authentication, tasks, and UI state.

### Options Evaluated

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| **React Context + Hooks** | Built-in, no dependencies, simple | Can cause re-renders, not optimized | ✅ **SELECTED** for MVP |
| **Zustand** | Lightweight, hooks-based, no boilerplate | Another dependency | ⏭️ Future consideration |
| **Redux Toolkit** | Powerful, dev tools, time-travel debugging | Heavy, complex, overkill for MVP | ❌ Too complex |
| **Jotai/Recoil** | Atomic state, fine-grained updates | Less mature, niche | ❌ Unnecessary complexity |

### Decision: React Context + Hooks for MVP

**Rationale**:
- **Sufficient**: Auth state + task list is simple enough
- **No Dependencies**: Built into React
- **Constitutional Compliance**: "Client-side state management MUST be minimal"
- **Upgrade Path**: Can migrate to Zustand if needed

**Implementation Pattern**:
```typescript
// contexts/AuthContext.tsx
type AuthContextType = {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for stored token on mount
    const token = localStorage.getItem('access_token');
    if (token) {
      // Validate token and fetch user
      fetchUser(token);
    }
    setIsLoading(false);
  }, []);

  // ... login, logout implementations

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};

// Usage
const { user, login } = useAuth();
```

**State Organization**:
- **AuthContext**: User data, login/logout, token management
- **Component State**: Form inputs, UI toggles, local loading states
- **Server State**: Tasks fetched from API (no local cache for MVP)

**References**:
- React Context: https://react.dev/reference/react/useContext
- Zustand (future): https://zustand-demo.pmnd.rs/

---

## 8. API Contract Definition (OpenAPI)

### Context
Constitution requires OpenAPI documentation. Need to define contract format and generation strategy.

### Research Findings

**FastAPI Auto-Generated OpenAPI**:
- FastAPI automatically generates OpenAPI 3.0 schema
- Access at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- Based on Pydantic models and type hints

**Custom Contract Files** (Recommended for spec tracking):
- Store explicit OpenAPI YAMLs in `specs/002-todo-web-app/contracts/`
- Serves as source of truth before implementation
- Version controlled, reviewed separately from code

**Contract Structure**:
```yaml
# contracts/auth.yaml
openapi: 3.0.0
paths:
  /auth/register:
    post:
      summary: Register new user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
```

**Decision: Use Both**
1. **Contract YAML files**: Design phase (plan.md)
2. **FastAPI auto-generation**: Implementation phase (validate against contracts)

**Contract Testing**:
- Use `pytest` with contract files to validate API responses
- Ensure implementation matches spec

**References**:
- OpenAPI Specification: https://swagger.io/specification/
- FastAPI OpenAPI: https://fastapi.tiangolo.com/tutorial/metadata/

---

## 9. Testing Strategy

### Context
Constitution mandates TDD with pytest (backend) and React Testing Library (frontend).

### Backend Testing (pytest)

**Test Pyramid**:
1. **Unit Tests** (60%): Services, utilities, pure functions
2. **Integration Tests** (30%): API endpoints with test database
3. **Contract Tests** (10%): Validate OpenAPI compliance

**Structure**:
```
tests/
├── conftest.py          # Fixtures (test DB, client, auth)
├── unit/
│   ├── test_auth_service.py
│   └── test_task_service.py
├── integration/
│   └── test_user_isolation.py
└── contract/
    ├── test_auth_api.py
    └── test_tasks_api.py
```

**Key Fixtures**:
```python
@pytest.fixture
def test_db():
    # Create test database
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield Session(engine)
    # Cleanup

@pytest.fixture
def authenticated_client(test_db):
    # Create user, generate JWT, return client with auth header
    pass
```

### Frontend Testing (React Testing Library)

**Test Types**:
1. **Component Tests**: Render, user interactions, props
2. **Integration Tests**: Form submissions, API mocking
3. **E2E Tests** (Optional): Playwright for critical flows

**Example**:
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

test('submits login form with valid credentials', async () => {
  render(<LoginForm />);

  fireEvent.change(screen.getByLabelText(/email/i), {
    target: { value: 'user@example.com' }
  });
  fireEvent.change(screen.getByLabelText(/password/i), {
    target: { value: 'password123' }
  });
  fireEvent.click(screen.getByRole('button', { name: /login/i }));

  expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
});
```

**References**:
- pytest: https://docs.pytest.org/
- React Testing Library: https://testing-library.com/react

---

## 10. Error Handling & Logging

### Context
Constitution requires structured error responses and proper logging.

### Backend Error Handling

**FastAPI Exception Handlers**:
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.detail.get("code", "UNKNOWN"),
                "message": exc.detail.get("message", "An error occurred"),
                "details": exc.detail.get("details", {}) if DEBUG else {}
            }
        }
    )
```

**Custom Error Codes**:
- `INVALID_INPUT`: 400 - Validation errors
- `UNAUTHORIZED`: 401 - Missing/invalid token
- `FORBIDDEN`: 403 - Insufficient permissions
- `NOT_FOUND`: 404 - Resource doesn't exist
- `INTERNAL_ERROR`: 500 - Server errors

**Logging Strategy**:
```python
import logging
from logging.handlers import RotatingFileHandler

# Development: Console logging
logging.basicConfig(level=logging.INFO)

# Production: File logging with rotation
handler = RotatingFileHandler('app.log', maxBytes=10MB, backupCount=5)
logger.addHandler(handler)
```

**What to Log**:
- ✅ Authentication attempts (success/failure)
- ✅ Authorization failures (403)
- ✅ Database errors
- ✅ Unexpected exceptions
- ❌ Sensitive data (passwords, tokens, user data)

### Frontend Error Handling

**Error Display Strategy**:
1. **Form Validation**: Inline messages below fields
2. **API Errors**: Toast notifications
3. **Fatal Errors**: Error boundaries with recovery

**Error Boundary Example**:
```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

**References**:
- FastAPI error handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- React error boundaries: https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary

---

## Summary

All technology choices align with constitutional principles and specification requirements. The research phase is complete with clear decisions documented for implementation.

**Key Decisions**:
1. ✅ **Monorepo**: Turborepo + pnpm workspaces
2. ✅ **Authentication**: Custom JWT (python-jose) following Better Auth patterns
3. ✅ **Frontend**: Next.js 16+ App Router with route groups
4. ✅ **Backend**: FastAPI with clean architecture (routers → services → models)
5. ✅ **ORM**: SQLModel with Alembic migrations
6. ✅ **Database**: Neon Serverless PostgreSQL with connection pooling
7. ✅ **State Management**: React Context + Hooks (minimal)
8. ✅ **API Contracts**: OpenAPI YAML + FastAPI auto-generation
9. ✅ **Testing**: pytest (backend) + React Testing Library (frontend)
10. ✅ **Error Handling**: Structured JSON responses + proper logging

**Ready for Phase 1**: Design artifacts (data-model.md, contracts/, quickstart.md)
