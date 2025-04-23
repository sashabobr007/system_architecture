# from datetime import datetime
# from models.task import Goal, Task, TaskStatus
#
# fake_goals_db = {}
# fake_tasks_db = {}
# current_goal_id = 1
# current_task_id = 1
#
# # Инициализация тестовыми данными
#
# goal = Goal(
#     id=current_goal_id,
#     title="Изучить FastAPI",
#     description="Полный курс по FastAPI",
#     owner_id='admin',
#     created_at=datetime.now()
# )
# fake_goals_db['1'] = goal
#
# task = Task(
#     id=current_task_id,
#     title="Написать первый API",
#     description="Создать простой эндпоинт",
#     goal_id=goal.id,
#     owner_id='admin',
#     status=TaskStatus.TODO,
#     created_at=datetime.now(),
#     updated_at=datetime.now()
# )
# fake_tasks_db['1'] = task