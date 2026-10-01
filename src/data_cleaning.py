"""Load and validate the project's distinct India and global data layers."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def clean_india() -> tuple[pd.DataFrame, pd.DataFrame]:
    national = pd.read_csv(PROCESSED / "india_national_trends.csv")
    states = pd.read_csv(PROCESSED / "india_state_accidents.csv")
    for frame in (national, states):
        frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype("int16")
    for column in ("accidents", "fatalities", "persons_injured"):
        if column in national:
            national[column] = pd.to_numeric(national[column], errors="coerce")
            if national[column].isna().any() or (national[column] < 0).any():
                raise ValueError(f"Invalid values in India national {column}")
    states["accidents"] = pd.to_numeric(states["accidents"], errors="coerce")
    states["fatalities"] = pd.to_numeric(states["fatalities"], errors="coerce")
    # NA is retained as missing (Ladakh has no 2020 value in this source table).
    if (states["accidents"].dropna() < 0).any():
        raise ValueError("Negative state accident count found")
    if (states["fatalities"].dropna() < 0).any():
        raise ValueError("Negative state fatalities found")
    if states.duplicated(["state_ut", "year"]).any():
        raise ValueError("Duplicate state/UT-year rows found")
    states["fatalities_per_100_accidents"] = (
        states["fatalities"] / states["accidents"] * 100
    )
    national["fatalities_per_100_accidents"] = (
        national["fatalities"] / national["accidents"] * 100
    )
    national["injuries_per_100_accidents"] = (
        national["persons_injured"] / national["accidents"] * 100
    )
    return national, states


def clean_violations() -> pd.DataFrame:
    violations = pd.read_csv(PROCESSED / "india_traffic_violations.csv")
    violations["year"] = pd.to_numeric(violations["year"], errors="raise").astype("int16")
    for column in ("accidents", "fatalities"):
        violations[column] = pd.to_numeric(violations[column], errors="raise")
        if (violations[column] < 0).any():
            raise ValueError(f"Negative traffic-rule category value in {column}")
    if violations.duplicated(["category", "year"]).any():
        raise ValueError("Duplicate traffic-rule category/year rows found")
    return violations


def clean_global() -> pd.DataFrame:
    """Keep only documented WHO indicator fields; do not impute interval bounds."""
    source = ROOT / "data" / "raw" / "who_gho_rs_198.csv"
    raw = pd.read_csv(source)
    expected_code = "RS_198"
    if set(raw["IndicatorCode"].dropna().unique()) != {expected_code}:
        raise ValueError("WHO file contains unexpected indicator codes")
    if set(raw["Period"].dropna().astype(str).unique()) != {"2021"}:
        raise ValueError("Review source before processing a changed WHO year range")
    out = pd.DataFrame({
        "location_code": raw["SpatialDimValueCode"].astype("string"),
        "location": raw["Location"].astype("string").str.strip(),
        "parent_location_code": raw["ParentLocationCode"].astype("string"),
        "parent_location": raw["ParentLocation"].astype("string").str.strip(),
        "year": pd.to_numeric(raw["Period"], errors="raise").astype("int16"),
        "death_rate_per_100k": pd.to_numeric(raw["FactValueNumeric"], errors="coerce"),
        "lower_estimate": pd.to_numeric(raw["FactValueNumericLow"], errors="coerce"),
        "upper_estimate": pd.to_numeric(raw["FactValueNumericHigh"], errors="coerce"),
        "unit": raw["FactValueUoM"].astype("string"),
        "modified_at": raw["DateModified"].astype("string"),
    })
    if out.duplicated(["location_code", "year"]).any():
        raise ValueError("Duplicate WHO location-year rows found")
    if (out["death_rate_per_100k"].dropna() < 0).any():
        raise ValueError("Negative WHO death rate found")
    return out


def main() -> None:
    national, india_states = clean_india()
    global_data = clean_global()
    violations = clean_violations()
    national.to_csv(PROCESSED / "india_national_clean.csv", index=False)
    india_states.to_csv(PROCESSED / "india_state_accidents_clean.csv", index=False)
    global_data.to_csv(PROCESSED / "who_road_death_rate_clean.csv", index=False)
    violations.to_csv(PROCESSED / "india_traffic_violations_clean.csv", index=False)
    print(f"India national: {national.shape}; state panel: {india_states.shape}")
    print(f"WHO layer: {global_data.shape}; years: {global_data.year.unique().tolist()}")


if __name__ == "__main__":
    main()
