from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from models.task import Goal, GoalCreate, Task, TaskCreate, TaskStatus
from db.fake_db import fake_goals_db, fake_tasks_db, current_goal_id, current_task_id
from auth.dependencies import get_current_user
from exceptions import GoalNotFoundException


router = APIRouter(prefix="/goals", tags=["Goals"])


# Создание цели
@router.post("/", response_model=Goal)
async def create_goal(
        goal: GoalCreate,
        current_user=Depends(get_current_user)
):
    goal_id = len(fake_goals_db) + 1
    new_goal = Goal(
        id=goal_id,
        **goal.dict(),
        owner_id=current_user,
        created_at=datetime.now()
    )
    fake_goals_db[str(goal_id)] = new_goal
    return new_goal

# Получение всех целей пользователя
@router.get("/", response_model=List[Goal])
async def read_goals(current_user=Depends(get_current_user)):
    return [
        goal for goal in fake_goals_db.values()
        if goal.owner_id == current_user
    ]


# Получение всех задач цели
@router.get("/{goal_id}/tasks", response_model=List[Task])
async def read_goal_tasks(
        goal_id: int,
        current_user=Depends(get_current_user)):
    if goal_id not in fake_goals_db:
        raise GoalNotFoundException

    return [
        task for task in fake_tasks_db.values()
        if task.goal_id == goal_id
    ]

# Удаление цели (включая все задачи)
@router.delete("/goals/{goal_id}")
async def delete_goal(
        goal_id: int,
        current_user=Depends(get_current_user)):
    if goal_id not in fake_goals_db:
        raise GoalNotFoundException

    # Удаляем все связанные задачи
    task_ids = [t.id for t in fake_tasks_db.values() if t.goal_id == goal_id]
    for task_id in task_ids:
        del fake_tasks_db[task_id]

    del fake_goals_db[goal_id]
    return {"message": "Goal and all its tasks deleted successfully"}