from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models.task import Task, TaskStatus, TaskCreate
from db.fake_db import fake_tasks_db, fake_goals_db
from auth.dependencies import get_current_user
from exceptions import TaskNotFoundException, GoalNotFoundException

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Создание задачи в цели
@router.post("/{goal_id}/tasks", response_model=Task)
async def create_task_for_goal(
        goal_id: str,
        task: TaskCreate,
        current_user=Depends(get_current_user)
):

    if goal_id not in fake_goals_db:
        raise GoalNotFoundException

    task_id = len(fake_tasks_db) + 1
    new_task = Task(
        id=task_id,
        **task.dict(),
        goal_id=int(goal_id),
        owner_id=current_user,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    fake_tasks_db[str(task_id)] = new_task
    return new_task


# Обновление статуса задачи
@router.put("/{task_id}", response_model=Task)
async def update_task_status(
        task_id: str,
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
    task_id: str,
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
        task_id: str,
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
        task_id: str,
        current_user=Depends(get_current_user)):
    if task_id not in fake_tasks_db:
        raise TaskNotFoundException

    del fake_tasks_db[task_id]
    return {"message": "Task deleted successfully"}

