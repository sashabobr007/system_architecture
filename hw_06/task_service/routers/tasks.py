from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from models.task import Task, TaskStatus, TaskCreate
#from db.fake_db import fake_tasks_db, fake_goals_db
from auth.dependencies import get_current_user
from exceptions import TaskPermissionDeniedException, TaskNotFoundException,UserNotEnoughPermissions, GoalNotFoundException
from db.mongo import goals_collection, tasks_collection, parse_task, parse_goal
from bson import ObjectId


router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_object_id(id: str):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")


# Создание задачи в цели
@router.post("/{goal_id}/tasks", response_model=Task)
async def create_task_for_goal(
        goal_id: str,
        task: TaskCreate,
        current_user=Depends(get_current_user)
):
    obj_goal_id = get_object_id(goal_id)
    goal = goals_collection.find_one({"_id": obj_goal_id})

    if not goal:
        raise GoalNotFoundException

    task_data = task.dict()
    task_data.update({
        "goal_id": goal_id,
        "owner_id": current_user,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })

    result = tasks_collection.insert_one(task_data)
    new_task = tasks_collection.find_one({"_id": result.inserted_id})
    return parse_task(new_task)


# Обновление статуса задачи
@router.put("/{task_id}", response_model=Task)
async def update_task_status(
        task_id: str,
        status: TaskStatus,
        current_user=Depends(get_current_user)):
    obj_task_id = get_object_id(task_id)
    task = tasks_collection.find_one({"_id": obj_task_id})

    if not task:
        raise TaskNotFoundException
    if task["owner_id"] != current_user:
        raise UserNotEnoughPermissions

    update_data = {"status": status, "updated_at": datetime.now()}
    tasks_collection.update_one({"_id": obj_task_id}, {"$set": update_data})
    updated_task = tasks_collection.find_one({"_id": obj_task_id})
    return parse_task(updated_task)

# Назначение исполнителя задачи
@router.put("/{task_id}/assign", response_model=Task)
async def assign_task(
    task_id: str,
    username: str,
    current_user=Depends(get_current_user)):
    obj_task_id = get_object_id(task_id)
    task = tasks_collection.find_one({"_id": obj_task_id})

    if not task:
        raise TaskNotFoundException

    # Проверка, что текущий пользователь - владелец задачи
    if task["owner_id"] != current_user:
        raise TaskPermissionDeniedException

    # Здесь должна быть проверка, что username существует (запрос в User Service)

    update_data = {
        "assigned_user_id": username,
        "updated_at": datetime.now()
    }

    tasks_collection.update_one(
        {"_id": obj_task_id},
        {"$set": update_data}
    )

    updated_task = tasks_collection.find_one({"_id": obj_task_id})
    return parse_task(updated_task)

# Удаление исполнителя из задачи
@router.delete("/{task_id}/assign", response_model=Task)
async def unassign_task(
        task_id: str,
        current_user=Depends(get_current_user)):
    obj_task_id = get_object_id(task_id)
    task = tasks_collection.find_one({"_id": obj_task_id})

    if not task:
        raise TaskNotFoundException

    # Проверка прав:
    # Либо владелец задачи, либо назначенный исполнитель может снять назначение
    if task["owner_id"] != current_user and task.get("assigned_user_id") != current_user.id:
        raise TaskPermissionDeniedException

    update_data = {
        "assigned_user_id": None,
        "updated_at": datetime.now()
    }

    tasks_collection.update_one(
        {"_id": obj_task_id},
        {"$set": update_data}
    )

    updated_task = tasks_collection.find_one({"_id": obj_task_id})
    return parse_task(updated_task)

# Удаление задачи
@router.delete("/{task_id}")
async def delete_task(
        task_id: str,
        current_user=Depends(get_current_user)):
    obj_task_id = get_object_id(task_id)
    task = tasks_collection.find_one({"_id": obj_task_id})

    if not task:
        raise TaskNotFoundException
    if task["owner_id"] != current_user:
        raise UserNotEnoughPermissions

    tasks_collection.delete_one({"_id": obj_task_id})
    return {"message": "Task deleted successfully"}

