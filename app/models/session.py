from sqlalchemy import Column , Integer , String , DateTime ,func,ForeignKey,Float
from sqlalchemy.orm import relationship 

from app.database import Base

class Session(Base):
	__tablename__ = "sessions"
	
	id = Column(Integer , primary_key= True , index = True)
	user_id  = Column(Integer ,ForeignKey("users.id"),nullable = False)
	driver = Column(String , nullable = False )
	track = Column(String , nullable = False)
	session_type = Column(String, nullable = False )
	consistency_score = Column(Float, nullable=True)
	created_at = Column(DateTime , server_default = func.now())

	telemetry = relationship("Telemetry"  , back_populates = "session")
	lap_results = relationship("LapResult", back_populates = "session")

