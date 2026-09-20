import os
from typing import Tuple

_MODEL = None


def _get_asset_path(filename: str) -> str:
    # Look in the backend directory first, then the workspace root or cwd
    base = os.path.dirname(__file__)
    candidates = [
        os.path.join(base, filename),
        os.path.join(base, "..", filename),
        os.path.join(os.getcwd(), filename),
        os.path.join(os.getcwd(), "backend", filename),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.abspath(c)
    return os.path.abspath(os.path.join(base, "..", filename))


def load_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    
    # 1. Try native JSON format first (most compatible, zero pickle warnings)
    json_path = _get_asset_path("landslide_risk_model.json")
    if os.path.exists(json_path):
        try:
            import xgboost as xgb
            booster = xgb.Booster()
            booster.load_model(json_path)
            _MODEL = booster
            return _MODEL
        except Exception:
            pass

    # 2. Try joblib format
    joblib_path = _get_asset_path("landslide_risk_model.joblib")
    if os.path.exists(joblib_path):
        try:
            from joblib import load
            _MODEL = load(joblib_path)
            return _MODEL
        except Exception:
            pass

    _MODEL = None
    return _MODEL


def score_from_features(rain_1d: float, rain_3d: float, rain_5d: float, rain_7d: float) -> float:
    """Return a risk probability (0-1) using the supplied model."""
    model = load_model()
    if model is not None:
        try:
            import xgboost as xgb
            if isinstance(model, xgb.Booster):
                d = xgb.DMatrix(
                    [[float(rain_1d), float(rain_3d), float(rain_5d), float(rain_7d)]],
                    feature_names=['rain_1d', 'rain_3d', 'rain_5d', 'rain_7d']
                )
                pred = model.predict(d)[0]
                return float(pred)
            elif hasattr(model, "predict_proba"):
                features = [[float(rain_1d), float(rain_3d), float(rain_5d), float(rain_7d)]]
                proba = model.predict_proba(features)[0][1]
                return float(proba)
        except Exception:
            pass

    # Calibrated fallback: sustained rainfall > 100mm-150mm triggers HIGH/CRITICAL in Himalayas
    weighted_rain = (float(rain_1d) * 0.40) + (float(rain_3d) * 0.25) + (float(rain_5d) * 0.20) + (float(rain_7d) * 0.15)
    score = min(0.98, max(0.02, weighted_rain / 120.0))
    return round(float(score), 4)


def features_from_daily_list(daily_precip: list) -> Tuple[float, float, float, float]:
    """Given a list of up to 7 daily precipitation values (oldest first),
    compute cumulative 1/3/5/7 day sums where available.
    """
    vals = list(daily_precip)[-7:]
    # pad left if fewer than 7
    if len(vals) < 7:
        vals = [0.0] * (7 - len(vals)) + vals
    # most recent last
    rain_1d = sum(vals[-1:])
    rain_3d = sum(vals[-3:])
    rain_5d = sum(vals[-5:])
    rain_7d = sum(vals[-7:])
    return rain_1d, rain_3d, rain_5d, rain_7d
