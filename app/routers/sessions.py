from fastapi import APIRouter , HTTPException,Depends
from sqlalchemy.orm import Session as DBSession
from app.database import get_db
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate , SessionOut
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix ="/session" , tags =["sessions"])


@router.post("/",response_model = SessionOut)
def create_Session(payload:SessionCreate , db :DBSession = Depends(get_db), user: User = Depends(get_current_user)):
	session = SessionModel(user_id = user.id , **payload.model_dump())
	db.add(session)
	db.commit()
	db.refresh(session)
	return session

@router.get("/" , response_model = list[SessionOut] )
def list_Session(db: DBSession = Depends(get_db), user: User = Depends(get_current_user)):
	return db.query(SessionModel).filter(SessionModel.user_id == user.id).all()

@router.get("/{session_id}",response_model = SessionOut )
def get_session(session_id : int , db: DBSession = Depends(get_db) , user: User = Depends(get_current_user)):
	return db.query(SessionModel).filter(SessionModel.id == session_id , SessionModel.user_id == user.id).first()
