import pandas as pd 
from fastapi import APIRouter , UploadFile , File , Depends , HTTPException , status
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app.models.telemetry import Telemetry
from app.dependencies import get_current_user
from app.models.user import User
from app.models.session import Session as SessionModel
from app.workers.tasks import analyze_session_task

router = APIRouter(prefix = "/telemetry", tags =["telemetry"])

@router.post("/{session_id}/upload")
async def upload_telemetry(session_id : int , file: UploadFile  = File(...),db : DBSession = Depends(get_db), user : User = Depends(get_current_user)) :    

    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or unauthorized access"
        )
    

    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse CSV file: {str(e)}"
        )

    df = df.drop_duplicates()
    df = df.dropna(subset=["speed", "throttle", "lap"])

    records = [
        Telemetry(
            session_id=session_id,
            lap=int(row.lap),
            timestamp=str(row.timestamp),
            speed=float(row.speed),
            throttle=float(row.throttle),
            brake=float(row.brake),
            rpm=int(row.rpm),
            gear=int(row.gear),
        )
        for row in df.itertuples(index= False)
    ]
    db.bulk_save_objects(records)
    db.commit()

    job = analyze_session_task.delay(session_id)
    return {"status": "processing", "rows": len(records), "job_id": job.id}

