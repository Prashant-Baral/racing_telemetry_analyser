import csv
import random
import os
from datetime import timedelta

DRIVERS = ["VER", "HAM", "LEC", "NOR", "ALO"]
TRACKS = ["Silverstone", "Monza", "Suzuka", "Spa", "Interlagos"]
SESSION_TYPES = ["practice", "qualifying", "race"]

os.makedirs("data", exist_ok=True)

def generate_session_csv(session_index: int, driver: str, track: str, session_type: str, num_laps: int):
    filename = f"data/session_{session_index}_{driver}_{track}.csv"
    elapsed = timedelta(0)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["driver", "lap", "timestamp", "speed", "throttle", "brake", "rpm", "gear", "sector"])

        for lap in range(1, num_laps + 1):
            # occasionally simulate a slow/outlier lap (traffic, mistake, etc.)
            lap_is_slow = random.random() < 0.1

            for sector in range(1, 4):
                rows_in_sector = random.randint(15, 25)
                for _ in range(rows_in_sector):
                    step = timedelta(seconds=random.uniform(0.08, 0.15))
                    elapsed += step

                    speed = round(random.uniform(140, 330), 1)
                    if lap_is_slow:
                        speed *= 0.85  # slower lap = lower speeds across the board

                    total_seconds = elapsed.total_seconds()
                    hh = int(total_seconds // 3600)
                    mm = int((total_seconds % 3600) // 60)
                    ss = total_seconds % 60

                    writer.writerow([
                        driver, lap, f"{hh:02d}:{mm:02d}:{ss:06.3f}",
                        round(speed, 1),
                        round(random.uniform(0, 100), 1),
                        random.choice([0, 0, 0, 1]),
                        random.randint(9000, 12000),
                        random.randint(3, 8),
                        sector
                    ])

    return filename, {"driver": driver, "track": track, "session_type": session_type}

manifest = []
session_index = 1
for driver in DRIVERS:
    for _ in range(2):  # 2 sessions per driver, varied tracks/types
        track = random.choice(TRACKS)
        session_type = random.choice(SESSION_TYPES)
        num_laps = random.randint(8, 15)
        filename, meta = generate_session_csv(session_index, driver, track, session_type, num_laps)
        manifest.append({"file": filename, **meta})
        session_index += 1

with open("data/manifest.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["file", "driver", "track", "session_type"])
    writer.writeheader()
    writer.writerows(manifest)

print(f"Generated {len(manifest)} sessions. See data/manifest.csv for driver/track/type per file.")
