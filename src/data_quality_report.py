"""Document observed row counts, types, missingness, and key checks."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def frame_summary(label: str, frame: pd.DataFrame, key: list[str] | None = None) -> list[str]:
    lines = [f"## {label}", "", f"- Shape: {frame.shape[0]:,} rows × {frame.shape[1]} columns",
             f"- Duplicate complete rows: {int(frame.duplicated().sum()):,}"]
    if key:
        lines.append(f"- Duplicate `{', '.join(key)}` keys: {int(frame.duplicated(key).sum()):,}")
    date_columns = [column for column in frame.columns
                    if "date" in column.casefold() or "time" in column.casefold()]
    numeric = frame.select_dtypes(include="number").columns.tolist()
    categorical = [column for column in frame.columns if column not in numeric]
    lines.extend([
        f"- Date/time-like columns by name: {', '.join(date_columns) if date_columns else 'none'}",
        f"- Numeric columns: {', '.join(numeric) if numeric else 'none'}",
        f"- Categorical/text columns: {', '.join(categorical) if categorical else 'none'}",
        "- Column data types:",
        "",
        "```text",
        frame.dtypes.to_string(),
        "```",
        "- Columns with missing values:",
        "",
    ])
    missing = frame.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        lines.append("  - None")
    else:
        lines.extend(f"  - `{column}`: {int(count):,}" for column, count in missing.items())
    lines.append("")
    return lines


def main() -> None:
    raw_who = pd.read_csv(ROOT / "data/raw/who_gho_rs_198.csv")
    national = pd.read_csv(ROOT / "data/processed/india_national_clean.csv")
    states = pd.read_csv(ROOT / "data/processed/india_state_accidents_clean.csv")
    violations = pd.read_csv(ROOT / "data/processed/india_traffic_violations_clean.csv")
    who = pd.read_csv(ROOT / "data/processed/who_road_death_rate_clean.csv")
    lines = [
        "# Data quality and source inspection",
        "",
        "Generated from the preserved inputs and processed tables. This is a structural quality review, "
        "not a claim that source reporting is complete.",
        "",
    ]
    lines += frame_summary("Raw WHO export", raw_who, ["SpatialDimValueCode", "Period"])
    lines.extend([
        f"- Indicator codes: {', '.join(raw_who.IndicatorCode.dropna().unique().astype(str))}",
        f"- Indicator labels: {', '.join(raw_who.Indicator.dropna().unique().astype(str))}",
        f"- Periods: {', '.join(sorted(raw_who.Period.dropna().astype(str).unique()))}",
        f"- Locations: {raw_who.Location.nunique(dropna=True)}",
        f"- DateModified values: {', '.join(sorted(raw_who.DateModified.dropna().astype(str).unique()))}",
        "- Data type grouping follows observed file types; `Period` is numeric-looking text in the raw export and is converted to integer in the cleaned layer.",
        "",
    ])
    lines += frame_summary("Clean India national annual table", national, ["year"])
    lines += frame_summary("Clean India state/UT annual panel", states, ["state_ut", "year"])
    lines += frame_summary("Clean India traffic-rule categories", violations, ["category", "year"])
    lines += frame_summary("Clean WHO country/area panel", who, ["location_code", "year"])
    lines.extend([
        "## Cleaning decisions",
        "",
        "- WHO interval-bound fields are empty in the supplied CSV and remain null; no confidence bounds are invented.",
        "- WHO source disaggregation fields are empty; the analysis uses the documented indicator-level numeric fact.",
        "- Zero values are retained as source values and are not changed into missing values.",
        "- The 2020 Ladakh NA remains null. The 2020 Jammu and Kashmir footnote is stored in `source_note`.",
        "- Source asterisks on Dadra & Nagar Haveli's 2021-2022 observations are retained as a note; the annex does not explain them.",
        "- State and national totals and traffic-rule category totals reconcile for accidents and fatalities in each year 2020-2024.",
        "- No source file was overwritten; derived files are written under `data/processed/`.",
        "",
    ])
    output = ROOT / "reports/data_quality_summary.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
