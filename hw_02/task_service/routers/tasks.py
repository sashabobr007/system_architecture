from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models.task import Task, TaskStatus
from db.fake_db import fake_tasks_db
from auth.dependencies import get_current_user
from exceptions import TaskNotFoundException

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Обновление статуса задачи
@router.put("/{task_id}", response_model=Task)
async def update_task_status(
        task_id: int,
        status: TaskStatus,
        current_user=Depends(get_current_user)):
    if task_id not in fake_tasks_db:
        raise TaskNotFoundException

    task = fake_tasks_db[task_id]
    task.status = status
    task.updated_at = datetime.now()
    fake_tasks_db[task_id] = task
    return task

# Назначение исполнителя задачи
@router.put("/{task_id}/assign", response_model=Task)
async def assign_task(
    task_id: int,
    username: str,
    current_user=Depends(get_current_user)):
    if task_id not in fake_tasks_db:
        raise TaskNotFoundException

    task = fake_tasks_db[task_id]

    # Здесь должна быть проверка, что user_id существует (запрос в User Service)
    task.assigned_user_id = username
    task.updated_at = datetime.now()
    fake_tasks_db[task_id] = task
    return task

# Удаление исполнителя из задачи
@router.delete("/{task_id}/assign", response_model=Task)
async def unassign_task(
        task_id: int,
        current_user=Depends(get_current_user)):
    if task_id not in fake_tasks_db:
        raise TaskNotFoundException

    task = fake_tasks_db[task_id]
    task.assigned_user_id = None
    task.updated_at = datetime.now()
    fake_tasks_db[task_id] = task
    return task

# Удаление задачи
@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        current_user=Depends(get_current_user)):
    if task_id not in fake_tasks_db:
        raise TaskNotFoundException

    task = fake_tasks_db[task_id]
    del fake_tasks_db[task_id]
    return {"message": "Task deleted successfully"}

