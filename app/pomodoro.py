from fastapi import APIRouter
from datetime import datetime, timedelta
from .database import SessionLocal
from .models import Pomodoro

router = APIRouter(prefix="/pomodoro")

@router.post("/start")
def start_pomodoro():
    db = SessionLocal
    
    #verificando si ya hay un timer activo 
    
    active = db.query(Pomodoro).filter(Pomodoro.completed == False).first()
    if active: 
        db.close()
        return {"error": "Pomodoro already running"}
    
    pomo = Pomodoro()
    db.add(pomo)
    db.commit
    db.refresh(pomo)
    db.close()
    
    return {"message": "Pomodoro started", "id": pomo.id}

@router.get("/status")
def pomodoro_status():
    db = SessionLocal()
    pomo = db.query(Pomodoro).filter(Pomodoro.completed == False).first()
    
    if not pomo: 
        db.close()
        return {"status": "idle"}
    
    now = datetime.utcnow()
    end_time = pomo.start_time + timedelta(minutes=pomo.duration_minutes)
    remaining = (end_time - now).total_seconds()
    
    if remaining <= 0: 
        pomo.completed = True
        db.commit()
        db.close()
        return {"status": "completed"}
    
    db.close()
    return{
        "status": "running",
        "remaining_seconds": int(remaining)
           }
        