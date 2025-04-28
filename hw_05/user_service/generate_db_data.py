from faker import Faker
from passlib.context import CryptContext
from dao.dao import UsersDAO

# Настройка Faker для русских данных
fake = Faker('ru_RU')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


async def generate_users(count=100):
    try:
        users_data = []
        used_usernames = set()

        for i in range(count):
            # Генерация уникального username
            while True:
                first_name = fake.first_name()
                last_name = fake.last_name()
                base_username = f"{first_name.lower()}_{last_name.lower()}"
                random_number = fake.random_int(100, 99999)
                username = f"{base_username}_{random_number}"

                if username not in used_usernames:
                    used_usernames.add(username)
                    break

            # Формирование данных пользователя
            user_data = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{username}@example.com",
                "role": fake.random_element(elements=('user', 'owner')),
                "hashed_password": get_password_hash("password")
            }
            print(i)
            users_data.append(user_data)
            await UsersDAO.add(**user_data)
        print(f"Successfully inserted {count} users")
    except Exception as e:
        print(f"Error: {e}")