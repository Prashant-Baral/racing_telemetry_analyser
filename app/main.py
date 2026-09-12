from fastapi import FastAPI



app = FastAPI(title = " Racing Telemetry Analyzer")

@app.get("/health")
def health():
	return{ "status" : "ok"}
