"""Create one-step-ahead panel features without using future observations."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def add_lag_features(states: pd.DataFrame) -> pd.DataFrame:
    out = states.sort_values(["state_ut", "year"]).copy()
    out["previous_year_accidents"] = out.groupby("state_ut")["accidents"].shift(1)
    # Rows without a prior year cannot be used for this supervised prediction task.
    return out.dropna(subset=["accidents", "previous_year_accidents"])


def main() -> None:
    states = pd.read_csv(ROOT / "data/processed/india_state_accidents_clean.csv")
    features = add_lag_features(states)
    features.to_csv(ROOT / "data/processed/india_state_model_features.csv", index=False)
    print(f"Created {len(features)} lagged state-year observations.")


if __name__ == "__main__":
    main()
