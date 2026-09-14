from fastapi import FastAPI

from app.routers import auth , sessions , telemetry,analytics



app = FastAPI(title = " Racing Telemetry Analyzer")

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(telemetry.router)
app.include_router(analytics.router)



@app.get("/health")
def health():
	return{ "status" : "ok"}
