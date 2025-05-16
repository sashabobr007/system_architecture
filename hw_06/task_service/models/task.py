from enum import Enum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO

class Task(TaskCreate):
    id: str
    goal_id: str
    owner_id: str
    assigned_user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# class TaskBase(BaseModel):
#     title: str
#     description: Optional[str] = None
#     status: TaskStatus = TaskStatus.TODO
#
# class TaskCreate(TaskBase):
#     pass
#
# class Task(TaskBase):
#     id: int
#     goal_id: int
#     owner_id: str
#     assigned_user_id: Optional[str] = None
#     created_at: datetime
#     updated_at: datetime

# class GoalBase(BaseModel):
#     title: str
#     description: str
#
# class GoalCreate(GoalBase):
#     pass
#
# class Goal(GoalBase):
#     id: int
#     owner_id: str
#     created_at: datetime
#     tasks: Optional[List[Task]] = None

class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Goal(GoalCreate):
    id: str
    owner_id: str
    created_at: datetime
