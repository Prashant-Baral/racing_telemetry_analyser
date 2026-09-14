from pydantic import BaseModel

class LapStat(BaseModel):

	lap : int
	avg_speed : float
	max_speed : float
	avg_throttle : float 
	lap_time : float 

class SessionSummary(BaseModel):

	total_laps : int
	best_lap : float
	average_lap : float
	top_speed : float 
	average_speed : float 
	consistency_score : float 


class SectorStat(BaseModel):
	
	Sector : int
	avg_time : float
