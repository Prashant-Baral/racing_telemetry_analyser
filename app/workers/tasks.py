from app import models  # noqa: F401
from app.workers.celery_app import celery_app
from app.database import SessionLocal
from app.models.telemetry import LapResult
from app.models.session import Session as SessionModel
from app.services.analytics import load_telemetry_df, compute_lap_stats, compute_session_summary

@celery_app.task(name="analyze_session")
def analyze_session_task(session_id: int):
    db = SessionLocal()
    try:
        df = load_telemetry_df(db, session_id)
        if df.empty:
            return {"status": "no_data"}

        lap_stats = compute_lap_stats(df)
        summary = compute_session_summary(df, lap_stats)

        db.query(LapResult).filter(LapResult.session_id == session_id).delete()
        for lap in lap_stats:
            db.add(LapResult(
                session_id=session_id,
                lap=int(lap["lap"]),
                lap_time=lap["lap_time"],
                avg_speed=lap["avg_speed"],
                max_speed=lap["max_speed"],
            ))

        session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
        if session:
            session.consistency_score = summary["consistency_score"]

        db.commit()

        return {"status": "completed", "summary": summary}
    finally:
        db.close()
