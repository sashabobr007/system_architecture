from pymongo import MongoClient, ASCENDING
import os
from models.task import Goal, Task

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://mongo:27017/")
client = MongoClient(DATABASE_URL)
db = client['goals_tasks']
goals_collection = db['goals']
tasks_collection = db['tasks']

tasks_collection.create_index([("goal_id", ASCENDING)])

# Для просмотра индексов (В MongoDB индекс на поле _id создается автоматически для всех коллекций)
# def list_indexes(collection_name):
#     collection = db[collection_name]
#     indexes = collection.list_indexes()
#     print(f"Indexes for {collection_name}:")
#     for index in indexes:
#         print(index)
#
# list_indexes('goals')
# list_indexes('tasks')

def parse_task(task_data):
    task_data["id"] = str(task_data["_id"])
    del task_data["_id"]
    return Task(**task_data)


def parse_goal(goal_data):
    goal_data["id"] = str(goal_data["_id"])
    del goal_data["_id"]
    return Goal(**goal_data)