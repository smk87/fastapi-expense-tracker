from core.db import Base, engine
from fastapi import FastAPI

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the Expense Tracker API", "success": True}
