"""SQLModel base class for all models.

Constitution Principle IV: SQLModel ORM only, no raw SQL queries.
"""
from sqlmodel import SQLModel as _SQLModel
from typing import ClassVar
from pydantic import BaseModel


class SQLModel(_SQLModel):
    """Base class for all SQLModel models in the application."""

    __abstract__: ClassVar[bool] = True


__all__ = ["SQLModel"]