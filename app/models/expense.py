from datetime import datetime

from core.db import Base
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    show = Column(Boolean, default=True)
    amount = Column(Float, nullable=Float)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
