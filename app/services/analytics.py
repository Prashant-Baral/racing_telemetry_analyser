import numpy as np
import pandas as pd
from sqlalchemy.orm import Session as DBSession
from app.models.telemetry import Telemetry

def load_telemetry_df(db: DBSession, session_id: int) -> pd.DataFrame:
    rows = db.query(Telemetry).filter(Telemetry.session_id == session_id).all()
    data = [{
        "lap": r.lap, "timestamp": r.timestamp, "speed": r.speed,
        "throttle": r.throttle, "brake": r.brake, "rpm": r.rpm, "gear": r.gear
    } for r in rows]
    df = pd.DataFrame(data)
    if not df.empty:
        df["timestamp"] = pd.to_timedelta(df["timestamp"])
    return df

def compute_lap_stats(df: pd.DataFrame) -> list[dict]:
    agg = df.groupby("lap").agg(
        avg_speed=("speed", "mean"),
        max_speed=("speed", "max"),
        avg_throttle=("throttle", "mean"),
        lap_start=("timestamp", "min"),
        lap_end=("timestamp", "max"),
    ).reset_index()

    agg["lap_time"] = (agg["lap_end"] - agg["lap_start"]).dt.total_seconds()
    agg = agg.drop(columns=["lap_start", "lap_end"])

    return agg.round(2).to_dict(orient="records")


def compute_consistency_score(lap_times: list[float]) -> float:
    arr = np.array(lap_times)
    mean = arr.mean()
    std = arr.std()
    # simple learning-project metric: lower variance relative to mean = higher score
    score = max(0, 100 - (std / mean * 100))
    return round(float(score), 2)

def detect_outlier_laps(lap_times: list[float]) -> list[int]:
    arr = np.array(lap_times)
    q1, q3 = np.percentile(arr, [25, 75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [i for i, t in enumerate(lap_times) if t < lower or t > upper]

def compute_session_summary(df: pd.DataFrame, lap_stats: list[dict]) -> dict:
    lap_times = [l["lap_time"] for l in lap_stats]
    return {
        "total_laps": df["lap"].nunique(),
        "best_lap": round(min(lap_times), 2),
        "average_lap": round(float(np.mean(lap_times)), 2),
        "top_speed": round(df["speed"].max(), 2),
        "average_speed": round(df["speed"].mean(), 2),
        "consistency_score": compute_consistency_score(lap_times),
    }

def compute_sector_stats(df: pd.DataFrame, df_with_sector: pd.DataFrame) -> list[dict]:
    grouped = df_with_sector.groupby("sector").agg(avg_time=("speed", "mean")).reset_index()
    return grouped.round(2).to_dict(orient="records")
