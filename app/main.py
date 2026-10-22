from core.db import Base, engine
from fastapi import FastAPI
from routers.expense import expense_router

# Create Database Tables
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(expense_router)
