from models.user import UserInDB, UserRole

fake_users_db = {
    "admin": UserInDB(
        id=1,
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        role=UserRole.OWNER,
        disabled=False
    ),
    "user1": UserInDB(
        id=2,
        username="user1",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        role=UserRole.USER,
        disabled=False
    )
}