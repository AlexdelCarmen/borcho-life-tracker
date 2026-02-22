from sqlalchemy import Column, Integer, DateTime, String, Text
from datetime import datetime
from .database import Base

class Pomodoro(Base): 
    __tablename__ = "pomodoros"
    
    id = Column(Integer, primary_key = True, index=True)
    
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    
    session_type = Column(String, default="work")
    # work | shot_break | long_break    
    
    duration_minutes = Column(Integer, default=25)
    
    status = Column(String, default="running")
    # running | completed | interrupted
    
    focus_tag = Column(String, nullable=True)
    
    intensity = Column(Integer, nullable=True)
    
    notes = Column(Text, nullable=True)
    
    
    
    
    