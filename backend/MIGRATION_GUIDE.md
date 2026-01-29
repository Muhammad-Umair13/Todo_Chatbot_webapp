# Database Migration Guide

This guide explains how to work with the database schema and migrations for the Phase II Todo Web Application.

## How to Verify Tables in Neon

1. **Connect to Neon Console**:
   - Visit https://neon.tech/
   - Sign in to your Neon account
   - Select your project

2. **Using the SQL Editor**:
   ```sql
   -- Check if the task table exists and its structure
   \d task;

   -- View table schema
   SELECT column_name, data_type, is_nullable, column_default
   FROM information_schema.columns
   WHERE table_name = 'task';

   -- Count existing records
   SELECT COUNT(*) FROM task;
   ```

3. **Using psql (command line)**:
   ```bash
   # Connect using the connection string from Neon dashboard
   psql "postgres://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"

   # Then run the same SQL queries as above
   ```

## How to Run Migrations Locally

1. **Prerequisites**:
   - Python 3.13+ installed
   - PostgreSQL server running locally or accessible
   - Dependencies installed (`pip install -r requirements.txt`)

2. **Environment Setup**:
   ```bash
   # Create/edit .env file in the backend directory
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   JWT_SECRET=your-super-secret-jwt-key-change-in-production
   ```

3. **Running Migrations**:
   ```bash
   # Navigate to the backend directory
   cd backend

   # Upgrade to the latest migration
   alembic upgrade head

   # Downgrade to a specific revision
   alembic downgrade <revision_id>

   # Check current migration status
   alembic current

   # Show migration history
   alembic history
   ```

4. **Creating New Migrations**:
   ```bash
   # Generate a new migration based on model changes
   alembic revision --autogenerate -m "Description of changes"

   # Edit the generated migration file in alembic/versions/
   # Then apply the migration
   alembic upgrade head
   ```

## How Future Models Will Be Added

1. **Create the Model**:
   ```python
   # In backend/src/models/new_model.py
   from sqlmodel import SQLModel, Field
   from datetime import datetime
   from typing import Optional

   class NewModel(SQLModel, table=True):
       id: Optional[int] = Field(default=None, primary_key=True)
       name: str = Field(min_length=1, max_length=100)
       created_at: datetime = Field(default_factory=datetime.utcnow)

       # Add other fields as needed
   ```

2. **Update the Models Package**:
   ```python
   # In backend/src/models/__init__.py, add:
   from .new_model import NewModel

   __all__ = [
       # ... existing models
       "NewModel",
   ]
   ```

3. **Update Alembic Environment** (if not already configured):
   The env.py is already configured to import all models from the models package, so no additional changes are needed.

4. **Generate and Apply Migration**:
   ```bash
   # Generate migration based on model changes
   alembic revision --autogenerate -m "Add new_model table"

   # Apply the migration
   alembic upgrade head
   ```

5. **Create Service Layer** (optional but recommended):
   ```python
   # In backend/src/services/new_model_service.py
   from sqlmodel import Session, select
   from ..models.new_model import NewModel

   class NewModelService:
       @staticmethod
       def get_all(session: Session):
           # Implementation
           pass
   ```

6. **Create API Endpoints** (if needed):
   ```python
   # In backend/src/routers/new_model.py
   from fastapi import APIRouter, Depends
   from sqlmodel import Session
   from ..database import get_session
   from ..models.new_model import NewModel

   router = APIRouter(prefix="/api/new-models", tags=["new-models"])

   @router.get("/")
   def get_new_models(session: Session = Depends(get_session)):
       # Implementation
       pass
   ```

## Migration Best Practices

1. **Always backup your database** before running migrations in production
2. **Test migrations** on a copy of production data first
3. **Keep migrations backward compatible** when possible
4. **Use descriptive migration messages** to understand the purpose
5. **Review generated migrations** before applying them
6. **Handle data migrations** separately if needed (using data migration scripts)

## Troubleshooting

- **Alembic not detecting model changes**: Make sure your model is imported in the models package `__init__.py`
- **Migration conflicts**: Use `alembic merge` to resolve branching conflicts
- **Rollback issues**: Always test downgrade operations in development first
- **Connection errors**: Verify your DATABASE_URL in the .env file