# Quickstart: Local Development Setup

**Feature**: 002-todo-web-app
**Date**: 2026-01-05
**Purpose**: Guide for setting up local development environment

## Overview

This guide walks you through setting up the full-stack Todo application for local development. The monorepo contains a Next.js frontend (`apps/web`) and FastAPI backend (`apps/api`).

---

## Prerequisites

### Required Software

- **Node.js**: v20+ ([Download](https://nodejs.org/))
- **pnpm**: v8+ (Install: `npm install -g pnpm`)
- **Python**: 3.13+ ([Download](https://www.python.org/downloads/))
- **PostgreSQL**: 14+ ([Download](https://www.postgresql.org/download/)) or use Neon
- **Git**: Latest version

### Verify Installations

```bash
node --version  # Should be v20+
pnpm --version  # Should be v8+
python --version  # Should be 3.13+
psql --version  # Should be 14+
git --version
```

---

## Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-app
git checkout 002-todo-web-app
```

### 2. Install Dependencies

**Root + Frontend**:
```bash
# Install root dependencies and workspace packages
pnpm install
```

**Backend**:
```bash
cd apps/api

# Option 1: Using Poetry (recommended)
poetry install

# Option 2: Using pip
pip install -e ".[dev]"

cd ../..
```

---

## Database Setup

### Option 1: Local PostgreSQL

**Create Database**:
```bash
psql -U postgres
CREATE DATABASE todo_dev;
CREATE USER todo_user WITH ENCRYPTED PASSWORD 'dev_password';
GRANT ALL PRIVILEGES ON DATABASE todo_dev TO todo_user;
\q
```

**Connection String**:
```
DATABASE_URL=postgresql://todo_user:dev_password@localhost:5432/todo_dev
```

### Option 2: Neon Serverless (Recommended)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project: `todo-dev`
3. Copy the connection string
4. Use format: `postgresql://user:pass@ep-xxx.neon.tech/todo_dev?sslmode=require`

---

## Environment Configuration

### Frontend Environment

Create `apps/web/.env.local`:
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Authentication
NEXT_PUBLIC_TOKEN_STORAGE=localStorage

# Development
NODE_ENV=development
```

### Backend Environment

Create `apps/api/.env`:
```bash
# Database
DATABASE_URL=postgresql://todo_user:dev_password@localhost:5432/todo_dev

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-min-32-characters-for-development-only
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
CORS_ORIGINS=http://localhost:3000
PASSWORD_HASH_ROUNDS=12

# Application
ENVIRONMENT=development
DEBUG=true
```

**⚠️ Security Note**: Never commit `.env` files. Use strong secrets in production.

---

## Database Migrations

### Run Initial Migration

```bash
cd apps/api

# Create initial migration
alembic revision --autogenerate -m "Create users and tasks tables"

# Apply migration
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
```

### Common Migration Commands

```bash
# Generate migration after model changes
alembic revision --autogenerate -m "Description"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current migration status
alembic current

# Show migration history
alembic history
```

---

## Running the Application

### Development Mode (All Services)

**Option 1: Turborepo (Recommended)**
```bash
# Run both frontend and backend in parallel
pnpm turbo dev

# Or run specific app
pnpm turbo dev --filter=web   # Frontend only
pnpm turbo dev --filter=api   # Backend only
```

**Option 2: Manual Start**

Terminal 1 - Backend:
```bash
cd apps/api
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd apps/web
pnpm dev
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## Testing

### Backend Tests

```bash
cd apps/api

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_auth_service.py

# Run specific test
pytest tests/unit/test_auth_service.py::test_register_user
```

### Frontend Tests

```bash
cd apps/web

# Run all tests
pnpm test

# Run in watch mode
pnpm test:watch

# Run with coverage
pnpm test:coverage
```

### Contract Tests

```bash
cd apps/api
pytest tests/contract/ -v
```

---

## Code Quality

### Linting & Formatting

**Frontend**:
```bash
cd apps/web

# Run ESLint
pnpm lint

# Fix auto-fixable issues
pnpm lint:fix

# Format with Prettier
pnpm format
```

**Backend**:
```bash
cd apps/api

# Run Ruff linter
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/

# Format code with Black
black src/ tests/

# Check types with mypy
mypy src/
```

### Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Development Workflow

### Creating a New Feature

1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests first** (TDD):
   ```bash
   # Backend
   cd apps/api
   touch tests/unit/test_your_feature.py
   pytest tests/unit/test_your_feature.py  # Should fail (Red)
   ```

3. **Implement feature** (make tests pass):
   ```bash
   # Edit source files
   pytest  # Should pass (Green)
   ```

4. **Refactor**:
   ```bash
   # Clean up code
   pytest  # Should still pass
   ```

5. **Commit**:
   ```bash
   git add .
   git commit -m "feat: add your feature

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
   ```

### API Development Flow

1. **Define endpoint in contract** (`specs/002-todo-web-app/contracts/`)
2. **Write contract test** (`tests/contract/`)
3. **Implement router** (`src/routers/`)
4. **Implement service** (`src/services/`)
5. **Run contract test** (validate against spec)
6. **Test manually** via Swagger UI

---

## Troubleshooting

### Database Connection Issues

**Symptom**: `sqlalchemy.exc.OperationalError`

**Solution**:
```bash
# Verify DATABASE_URL in .env
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1;"

# Check PostgreSQL is running
pg_ctl status  # or: brew services list (macOS)
```

### Port Already in Use

**Symptom**: `Error: listen EADDRINUSE: address already in use :::3000`

**Solution**:
```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process
kill -9 <PID>
```

### Module Not Found

**Symptom**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**:
```bash
# Backend
cd apps/api
poetry install  # or: pip install -e ".[dev]"

# Frontend
cd apps/web
pnpm install
```

### Migration Conflicts

**Symptom**: `alembic.util.exc.CommandError: Can't locate revision`

**Solution**:
```bash
cd apps/api

# Reset to clean state (development only!)
alembic downgrade base
alembic upgrade head

# Or delete and recreate database (nuclear option)
dropdb todo_dev
createdb todo_dev
alembic upgrade head
```

---

## Useful Commands

### Monorepo Commands (from root)

```bash
# Install all dependencies
pnpm install

# Run all apps in dev mode
pnpm turbo dev

# Build all apps
pnpm turbo build

# Run all tests
pnpm turbo test

# Lint all code
pnpm turbo lint

# Clean all build artifacts
pnpm turbo clean
```

### Backend Commands

```bash
cd apps/api

# Start development server
uvicorn src.main:app --reload

# Run tests with coverage
pytest --cov=src

# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Interactive shell
python -m src.main  # or: poetry run python
```

### Frontend Commands

```bash
cd apps/web

# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run tests
pnpm test

# Type check
pnpm typecheck
```

---

## Next Steps

1. ✅ Environment set up and running
2. ⏭️ Run `/sp.tasks` to generate executable task list
3. ⏭️ Implement features following TDD (Red-Green-Refactor)
4. ⏭️ Run tests after each feature
5. ⏭️ Create PR when user story is complete

**Ready to Start Development!** 🚀

---

## Additional Resources

- **Next.js Docs**: https://nextjs.org/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLModel Docs**: https://sqlmodel.tiangolo.com
- **Turborepo Docs**: https://turbo.build/repo/docs
- **Alembic Docs**: https://alembic.sqlalchemy.org
- **Neon Docs**: https://neon.tech/docs

## Support

For issues or questions:
- Check troubleshooting section above
- Review specification: `specs/002-todo-web-app/spec.md`
- Review architecture: `specs/002-todo-web-app/plan.md`
- Check API contracts: `specs/002-todo-web-app/contracts/`
