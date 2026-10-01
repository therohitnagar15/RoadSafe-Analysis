"""Compare a carry-forward baseline to a small time-aware regression experiment."""
from pathlib import Path
import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from joblib import dump

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["previous_year_accidents", "year", "state_ut"]


def score(name: str, actual: np.ndarray, predicted: np.ndarray) -> dict[str, float | str]:
    return {
        "model": name,
        "mae": float(mean_absolute_error(actual, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "r2": float(r2_score(actual, predicted)),
    }


def main() -> None:
    data = pd.read_csv(ROOT / "data/processed/india_state_model_features.csv")
    # Train only on outcomes through 2023. All 2024 state rows form the final holdout.
    train = data[data["year"] <= 2023].copy()
    test = data[data["year"] == 2024].copy()
    if train.empty or test.empty:
        raise ValueError("Expected training rows through 2023 and a 2024 holdout")
    numeric = ["previous_year_accidents", "year"]
    categorical = ["state_ut"]
    prep = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]), numeric),
        ("state", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])
    candidates = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=300, min_samples_leaf=2, random_state=42, n_jobs=-1
        ),
    }
    actual = test["accidents"].to_numpy(dtype=float)
    results = [score("last_year_baseline", actual,
                     test["previous_year_accidents"].to_numpy(dtype=float))]
    predictions = test[["state_ut", "year", "previous_year_accidents", "accidents"]].copy()
    predictions = predictions.rename(columns={"accidents": "actual_accidents"})
    predictions["last_year_baseline"] = test["previous_year_accidents"].to_numpy()
    interpretations = []
    for name, estimator in candidates.items():
        pipeline = Pipeline([("prep", prep), ("model", estimator)])
        pipeline.fit(train[FEATURES], train["accidents"])
        model_dir = ROOT / "models"
        model_dir.mkdir(exist_ok=True)
        dump(pipeline, model_dir / f"{name}.joblib")
        pred = np.maximum(0, pipeline.predict(test[FEATURES]))
        results.append(score(name, actual, pred))
        predictions[name] = pred
        model = pipeline.named_steps["model"]
        feature_names = pipeline.named_steps["prep"].get_feature_names_out()
        values = model.coef_ if name == "linear_regression" else model.feature_importances_
        kind = "coefficient" if name == "linear_regression" else "feature_importance"
        interpretations.extend({"model": name, "feature": feature, "measure": kind,
                                "value": float(value)}
                               for feature, value in zip(feature_names, values))
    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    pd.DataFrame(results).to_csv(out / "model_metrics.csv", index=False)
    predictions.to_csv(out / "2024_state_predictions.csv", index=False)
    pd.DataFrame(interpretations).to_csv(out / "model_interpretation.csv", index=False)
    (out / "model_evaluation.json").write_text(
        json.dumps({
            "target": "reported state/UT road accident count",
            "train_years": sorted(train.year.unique().tolist()),
            "test_year": 2024,
            "test_rows": len(test),
            "warning": "One held-out year and 36 state/UT rows provide a small, weak basis for generalization.",
        }, indent=2), encoding="utf-8"
    )
    print(pd.DataFrame(results).to_string(index=False))
    print(f"2024 holdout rows: {len(test)}; metrics: {out / 'model_metrics.csv'}")


if __name__ == "__main__":
    main()
