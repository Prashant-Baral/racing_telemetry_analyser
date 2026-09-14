from fastapi import APIRouter  , Depends , HTTPException
from sqlalchemy.orm import Session as DBSession
from app.models.user import User
from app.database import get_db

from app.dependencies import get_current_user
from app.services.analytics import load_telemetry_df , compute_lap_stats , compute_session_summary 


router = APIRouter(prefix = "/analytics" , tags=["analytics"])

@router.get("/{session_id}/laps")
def get_lap_stats(session_id : int , db: DBSession = Depends(get_db) , user : User = Depends(get_current_user)):
	df = load_telemetry_df(db, session_id)
	return compute_lap_stats(df)

@router.get("/{session_id}/summary")
def get_summary(session_id: int, db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
    df = load_telemetry_df(db, session_id)
    lap_stats = compute_lap_stats(df)
    return compute_session_summary(df, lap_stats)

