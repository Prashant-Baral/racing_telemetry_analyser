from pydantic_settings import BaseSettings

class Settings(BaseSettngs):
	database_url : str
	redis_url : str
	secret_key : str

	class config:
		env_file =".env"


settings = Settings()


