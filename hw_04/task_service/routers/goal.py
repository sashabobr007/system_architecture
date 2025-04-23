from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from models.task import Goal, GoalCreate, Task, TaskCreate, TaskStatus
#from db.fake_db import fake_goals_db, fake_tasks_db, current_goal_id, current_task_id
from auth.dependencies import get_current_user
from exceptions import GoalNotFoundException, UserNotEnoughPermissions
from db.mongo import goals_collection, tasks_collection, parse_task, parse_goal
from bson import ObjectId


router = APIRouter(prefix="/goals", tags=["Goals"])

def get_object_id(id: str):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")


# Создание цели
@router.post("/", response_model=Goal)
async def create_goal(
        goal: GoalCreate,
        current_user=Depends(get_current_user)
):
    goal_data = goal.dict()
    goal_data["owner_id"] = current_user
    goal_data["created_at"] = datetime.now()

    result = goals_collection.insert_one(goal_data)
    new_goal = goals_collection.find_one({"_id": result.inserted_id})
    return parse_goal(new_goal)


# Получение всех целей пользователя
@router.get("/", response_model=List[Goal])
async def read_goals(current_user=Depends(get_current_user)):
    goals = goals_collection.find({"owner_id": current_user})
    return [parse_goal(goal) for goal in goals]


# Получение всех задач цели
@router.get("/{goal_id}/tasks", response_model=List[Task])
async def read_goal_tasks(
        goal_id: str,
        current_user=Depends(get_current_user)):
    obj_goal_id = get_object_id(goal_id)
    goal = goals_collection.find_one({"_id": obj_goal_id})

    if not goal:
        raise GoalNotFoundException
    if goal["owner_id"] != current_user:
        raise UserNotEnoughPermissions

    tasks = tasks_collection.find({"goal_id": goal_id})
    return [parse_task(task) for task in tasks]

# Удаление цели (включая все задачи)
@router.delete("/goals/{goal_id}")
async def delete_goal(
        goal_id: str,
        current_user=Depends(get_current_user)):
    obj_goal_id = get_object_id(goal_id)
    goal = goals_collection.find_one({"_id": obj_goal_id})

    if not goal:
        raise GoalNotFoundException
    if goal["owner_id"] != current_user:
        raise UserNotEnoughPermissions

    goals_collection.delete_one({"_id": obj_goal_id})
    tasks_collection.delete_many({"goal_id": goal_id})
    return {"message": "Goal and all its tasks deleted successfully"}