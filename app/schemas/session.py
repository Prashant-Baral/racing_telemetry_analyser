from pydantic import BaseModel 
from datetime import datetime

class SessionCreate(BaseModel):
	
	driver : str
	track : str
	session_type : str

class SessionOut(BaseModel):

	id: int
	driver : str
	track : str
	session_type : str
	created_at : datetime

	class config:
		from_attributes = True

