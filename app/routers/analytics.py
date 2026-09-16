from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.models.user import User
from app.models.session import Session as SessionModel
from app.models.telemetry import LapResult
from app.database import get_db

from app.dependencies import get_current_user

from celery.result import AsyncResult
from app.workers.celery_app import celery_app

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/{session_id}/laps")
def get_lap_stats(session_id: int, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    laps = db.query(LapResult).filter(LapResult.session_id == session_id).all()
    if not laps:
        raise HTTPException(
            status_code=404,
            detail="No analysis results yet — upload telemetry first, or check job status"
        )

    return [
        {
            "lap": l.lap,
            "lap_time": l.lap_time,
            "avg_speed": l.avg_speed,
            "max_speed": l.max_speed,
        }
        for l in laps
    ]


@router.get("/{session_id}/summary")
def get_summary(session_id: int, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    laps = db.query(LapResult).filter(LapResult.session_id == session_id).all()
    if not laps:
        raise HTTPException(
            status_code=404,
            detail="No analysis results yet — upload telemetry first, or check job status"
        )

    lap_times = [l.lap_time for l in laps]
    return {
        "total_laps": len(laps),
        "best_lap": round(min(lap_times), 2),
        "average_lap": round(sum(lap_times) / len(lap_times), 2),
        "top_speed": round(max(l.max_speed for l in laps), 2),
        "average_speed": round(sum(l.avg_speed for l in laps) / len(laps), 2),
	"consistency_score": session.consistency_score,
    }


@router.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    result = AsyncResult(job_id, app=celery_app)
    return {"status": result.status, "result": result.result if result.ready() else None}
