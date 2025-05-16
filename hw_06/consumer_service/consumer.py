# consumer.py (отдельный сервис)
import asyncio
from aiokafka import AIOKafkaConsumer
import json
from dao.dao import UsersDAO


async def consume_users():
    consumer = AIOKafkaConsumer(
        'user_created',
        bootstrap_servers='kafka1:9092,kafka2:9092',
        group_id='user_consumer_group'
    )

    await consumer.start()
    try:
        async for msg in consumer:
            try:
                user_data = json.loads(msg.value.decode())
                # Запись в базу данных
                await UsersDAO.add(**user_data)
                print(f"User {user_data['username']} saved to DB")
            except Exception as e:
                print(f"Error processing message: {str(e)}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_users())