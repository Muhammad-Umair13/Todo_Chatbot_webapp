"""Task API endpoints.

Constitution Principle VII: Pure REST API with stateless operations.
Constitution Principle III: JWT required on all protected routes.
Constitution Principle III: Ownership enforced in every query.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..auth.dependencies import require_user_id
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse


router = APIRouter(prefix="/api", tags=["tasks"], redirect_slashes=False)


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    user_id: str = Depends(require_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        task_create: Task data from request body
        user_id: Extracted from JWT token via dependency
        session: Database session from dependency

    Returns:
        TaskResponse: The created task with all fields

    Raises:
        HTTPException: 422 if validation fails
        HTTPException: 401 if authentication fails
    """
    return TaskService.create_task(session, task_create, user_id)


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    user_id: str = Depends(require_user_id),
    completed: bool = None,
    session: Session = Depends(get_session)
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user with optional completion filter.

    Args:
        user_id: Extracted from JWT token via dependency
        completed: Optional filter for completion status (None = all tasks)
        session: Database session from dependency

    Returns:
        List[TaskResponse]: List of tasks for the user
    """
    return TaskService.get_tasks(session, user_id, completed)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user_id: str = Depends(require_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Get a specific task by ID for the authenticated user.

    Args:
        task_id: ID of the task to retrieve
        user_id: Extracted from JWT token via dependency
        session: Database session from dependency

    Returns:
        TaskResponse: The requested task

    Raises:
        HTTPException: 404 if task not found or not owned by user
    """
    task = TaskService.get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(require_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Update a specific task for the authenticated user.

    Args:
        task_id: ID of the task to update
        task_update: Update data from request body
        user_id: Extracted from JWT token via dependency
        session: Database session from dependency

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: 404 if task not found or not owned by user
        HTTPException: 422 if validation fails
    """
    task = TaskService.update_task(session, task_id, user_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def partial_update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(require_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Partially update a specific task for the authenticated user.

    Args:
        task_id: ID of the task to update
        task_update: Partial update data from request body
        user_id: Extracted from JWT token via dependency
        session: Database session from dependency

    Returns:
        TaskResponse: The updated task

    Raises:
        HTTPException: 404 if task not found or not owned by user
        HTTPException: 422 if validation fails
    """
    task = TaskService.update_task(session, task_id, user_id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    task_id: int,
    user_id: str = Depends(require_user_id),
    session: Session = Depends(get_session)
) -> TaskResponse:
    """
    Toggle the completion status of a specific task for the authenticated user.

    Args:
        task_id: ID of the task to toggle
        user_id: Extracted from JWT token via dependency
        session: Database session from dependency

    Returns:
        TaskResponse: The updated task with toggled completion status

    Raises:
        HTTPException: 404 if task not found or not owned by user
    """
    task = TaskService.toggle_task_completion(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: str = Depends(require_user_id),
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a specific task for the authenticated user.

    Args:
        task_id: ID of the task to delete
        user_id: Extracted from JWT token via dependency
        session: Database session from dependency

    Raises:
        HTTPException: 404 if task not owned by user (but not if already deleted)
    """
    # Attempt to delete the task - don't raise an error if it doesn't exist
    # This makes delete operations idempotent: deleting a non-existent task is OK
    TaskService.delete_task(session, task_id, user_id)


__all__ = ["router"]