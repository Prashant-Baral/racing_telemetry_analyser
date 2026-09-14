from fastapi import FastAPI

from app.routers import auth , sessions , telemetry



app = FastAPI(title = " Racing Telemetry Analyzer")

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(telemetry.router)



@app.get("/health")
def health():
	return{ "status" : "ok"}
