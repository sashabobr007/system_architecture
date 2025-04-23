import asyncio
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient
import random
from db.mongo import goals_collection, tasks_collection

fake = Faker('ru_RU')
users = ['admin', 'user1', 'user2']

async def clear_collections():
    goals_collection.delete_many({})
    tasks_collection.delete_many({})
    print("Collections cleared")


async def seed_goals(num_goals=50, num_users=3):
    goals = []
    for i in range(num_goals):
        user_id = random.choice(users)
        goal = {
            "title": fake.sentence(nb_words=3),
            "description": fake.text(max_nb_chars=200),
            "owner_id": user_id,
            "created_at": datetime.now() - timedelta(days=random.randint(1, 30))
        }
        goals.append(goal)

    result = goals_collection.insert_many(goals)
    print(f"Inserted {len(result.inserted_ids)} goals")
    return result.inserted_ids


async def seed_tasks(goal_ids, num_tasks_per_goal=3, num_users=3):
    statuses = ["todo", "in_progress", "done"]
    tasks = []

    for goal_id in goal_ids:
        for _ in range(num_tasks_per_goal):
            user_id = random.choice(users)
            assigned_user = random.choice(users) if random.random() > 0.5 else None

            task = {
                "title": fake.sentence(nb_words=4),
                "description": fake.text(max_nb_chars=100),
                "status": random.choice(statuses),
                "goal_id": str(goal_id),
                "owner_id": user_id,
                "assigned_user_id": assigned_user,
                "created_at": datetime.now() - timedelta(days=random.randint(1, 30)),
                "updated_at": datetime.now() - timedelta(days=random.randint(0, 29))
            }
            tasks.append(task)

    result = tasks_collection.insert_many(tasks)
    print(f"Inserted {len(result.inserted_ids)} tasks")


async def generate():
    await clear_collections()
    goal_ids = await seed_goals()
    await seed_tasks(goal_ids)
    print("Database seeded successfully")