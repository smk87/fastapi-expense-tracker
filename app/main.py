from core.db import Base, engine
from fastapi import FastAPI
from routers.auth import auth_router
from routers.expense import expense_router
from routers.user import user_router

# Create Database Tables
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(expense_router)
app.include_router(user_router)
app.include_router(auth_router)
