

from fastapi import FastAPI
from routers import auth, tasks, goal

app = FastAPI(title="Task Service", version="1.0.0")
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(goal.router)

@app.get("/")
async def read_root():
    return {"Task Service": "Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
    #uvicorn.run(app, host="localhost", port=8002)