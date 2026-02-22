from fastapi import APIRouter
from datetime import datetime, timedelta
from .database import SessionLocal
from .models import Pomodoro

router = APIRouter(prefix="/pomodoro")

# --- Configuracion del Dojo ---

WORK_DURATION = 25
SHORT_BREAK_DURATION = 5
LONG_BREAK_DURATION = 15
CYCLES_BEFORE_LONG_BREAK = 4
ALLOWED_BREAK_OVERAGE_MINUTES = 2

@router.post("/start")
def start_pomodoro():
    db = SessionLocal()
    
    previous_status = None

    active = db.query(Pomodoro).filter(Pomodoro.status == "running").first()

    if active:
        now = datetime.utcnow()
        end_time = active.start_time + timedelta(minutes=active.duration_minutes)
        remaining = (end_time - now).total_seconds()

        if remaining <= 0:
            active.status = "completed"
            active.end_time = end_time
            previous_status = "completed"
        else:
            active.status = "interrupted"
            active.end_time = now
            previous_status = "interrupted"

        db.commit()

    # Crear nuevo pomodoro
    new_pomo = Pomodoro()
    db.add(new_pomo)
    db.commit()
    db.refresh(new_pomo)

    db.close()

    return {
        "message": "Pomodoro started",
        "id": new_pomo.id,
        "previous_status": previous_status
    }


@router.get("/status")
def pomodoro_status():
    db = SessionLocal()
    pomo = db.query(Pomodoro).filter(Pomodoro.status == "running").first()
    
    if not pomo: 
        db.close()
        return {"status": "idle"}
    
    now = datetime.utcnow()
    end_time = pomo.start_time + timedelta(minutes=pomo.duration_minutes)
    remaining = (end_time - now).total_seconds()
    
    if remaining <=0: 
        pomo.status = "completed"
        pomo.end_time = end_time
        db.commit()
        db.close()
        return {"status": "completed"}
    
    db.close()
    return {
        "status": "running",
        "remaining_seconds": int(remaining)
    }
    
@router.post("/interrupt")
def interrupt_pomodoro(): 
    db = SessionLocal()
    pomo = db.query(Pomodoro).filter(Pomodoro.status == "running").first()
    
    if not pomo: 
        db.close()
        return {"error": "No active pomodoro"}
    
    pomo.status = "interrupted"
    pomo.end_time = datetime.utcnow()
    db.commit()
    db.close()
    
    return {"message": "Pomodoro interrupted"}

@router.get("/stats")
def pomodoro_stats():
    db = SessionLocal()

    total_completed = db.query(Pomodoro).filter(Pomodoro.status == "completed").count()
    total_interrupted = db.query(Pomodoro).filter(Pomodoro.status == "interrupted").count()

    # Obtener historial ordenado del más reciente al más antiguo
    history = db.query(Pomodoro).order_by(Pomodoro.start_time.desc()).all()

    current_streak = 0

    for session in history:
        if session.status == "completed":
            current_streak += 1
        elif session.status == "interrupted":
            break
        else:
            # Ignorar sesiones running si existieran
            continue

    db.close()

    return {
        "total_completed": total_completed,
        "total_interrupted": total_interrupted,
        "current_streak": current_streak
    }
