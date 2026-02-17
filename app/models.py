from sqlalchemy import Column, Integer, DateTime, Boolean
from datetime import datetime
from .database import Base

class Pomodoro(Base): 
    __tablename__ = "pomodoros"
    
    id = Column(Integer, primary_key = True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    duration_minutes = Column(Integer, default=25)
    completed = Column(Boolean, default=False)
    
    
    
    