from fastapi import FastAPI
from routers import auth, users
from db import create_tables, delete_tables
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from generate_db_data import generate_users



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # await delete_tables()
    # await create_tables()
    # # Генерация пользователей
    # await generate_users(10)
    yield

app = FastAPI(lifespan=lifespan, title="User Service", version="1.0.0")
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"User Service": "Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    #uvicorn.run(app, host="localhost", port=8001)