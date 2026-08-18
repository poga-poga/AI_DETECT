from fastapi import FastAPI
from app.routers.users import router as users_router
from app.routers.logs import router as logs_router

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])

app.include_router(logs_router, prefix="/logs", tags=["logs"])
