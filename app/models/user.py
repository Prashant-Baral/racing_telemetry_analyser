from sqlalchemy import Column , Integer  , String , DateTime , func
from app.database import Base

class User(Base
):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True , index = True)
	email = Column(String, unique = True , nullable = False , index = True)
	password_hash = Column(String , nullable = False)
	created_at = Column(DateTime , server_default = func.now())
