"""Build a small, reproducible explorer dataset from the local EEG CSV recordings.

Run: python prepare_data.py --source "C:/Users/HP/Epilipsy/CSV"
The original recordings are deliberately not copied into the public repository.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


def load_signal(path):
    with path.open(newline="", encoding="utf-8-sig") as file:
        rows = csv.reader(file)
        next(rows)
        return [float(row[0]) for row in rows if row and row[0].strip()]


def features(values):
    differences = [b - a for a, b in zip(values, values[1:])]
    crossings = sum((a < 0 <= b) or (a >= 0 > b) for a, b in zip(values, values[1:]))
    return [
        mean(values), pstdev(values), max(values) - min(values),
        math.sqrt(mean(v * v for v in values)),
        crossings / max(1, len(values) - 1),
        mean(abs(v) for v in differences),
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    records = []
    for stage in ("Interictal", "Preictal", "Ictal"):
        for path in sorted((args.source / stage).glob("*.csv")):
            signal = load_signal(path)
            if len(signal) < 32:
                continue
            records.append({"stage": stage.lower(), "name": path.stem, "length": len(signal),
                            "features": [round(x, 5) for x in features(signal)],
                            "signal": [round(x, 2) for x in signal[::max(1, len(signal) // 240)][:240]]})
    if not records:
        raise SystemExit("No usable recordings found")
    labels = ["Mean", "Variation", "Range", "RMS power", "Zero crossing", "Change rate"]
    summary = {stage.lower(): {label: round(mean(r["features"][i] for r in records if r["stage"] == stage.lower()), 3)
                               for i, label in enumerate(labels)} for stage in ("Interictal", "Preictal", "Ictal")}
    Path("data.json").write_text(json.dumps({"records": records, "summary": summary, "features": labels}, separators=(",", ":")), encoding="utf-8")
    print(f"Prepared {len(records)} recordings")


if __name__ == "__main__":
    main()
