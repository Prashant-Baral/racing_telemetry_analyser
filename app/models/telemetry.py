from sqlalchemy import Column , Integer , String , DateTime , func,ForeignKey,Float

from sqlalchemy.orm import relationship

from app.database import Base

class Telemetry(Base):
	__tablename__ = "telemetry"
	id = Column(Integer, primary_key = True , index = True)
	session_id = Column(Integer , ForeignKey("sessions.id"), nullable = False)
	lap = Column(Integer , nullable = False)
	timestamp = Column(String, nullable = False)
	speed = Column(Float)
	throttle = Column(Float)
	brake = Column(Float)
	rpm = Column(Float)
	gear = Column(Float)

	session = relationship("Session",back_populates = "telemetry")

class LapResult(Base):
	__tablename__ = "lap_results"
	
	id = Column(Integer, primary_key=True, index=True)
	session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
	lap = Column(Integer, nullable=False)
	lap_time = Column(Float)
	avg_speed = Column(Float)
	max_speed = Column(Float)
	session = relationship("Session", back_populates="lap_results")
 
