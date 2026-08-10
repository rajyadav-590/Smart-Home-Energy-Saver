import pickle
from pathlib import Path
import pandas as pd

ARTIFACT_DIR = Path("artifacts")

def predict_next_day_kwh(appliance, ds_next, avg_temp=30, hh_size=4, is_weekend=0):
    model_path = ARTIFACT_DIR / f"prophet_{appliance}.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # include all regressors expected by the model
    future = pd.DataFrame({
        "ds": [pd.to_datetime(ds_next)],
        "avg_temp": [avg_temp],
        "hh_size": [hh_size],
        "is_weekend": [is_weekend]
    })

    forecast = model.predict(future)

    predicted_kwh = float(forecast["yhat"].iloc[0])
    predicted_kwh = max(predicted_kwh, 1.0)

    return {
        "appliance": appliance,
        "predicted_kwh": round(predicted_kwh, 2)
    }