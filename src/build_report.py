"""Write an evidence-linked summary from the generated project outputs."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    national = pd.read_csv(ROOT / "data/processed/india_national_clean.csv")
    states = pd.read_csv(ROOT / "data/processed/india_state_accidents_clean.csv")
    violations = pd.read_csv(ROOT / "data/processed/india_traffic_violations_clean.csv")
    who = pd.read_csv(ROOT / "data/processed/who_road_death_rate_clean.csv")
    start, end = national.iloc[0], national.iloc[-1]
    state_latest = states[states.year == states.year.max()].nlargest(5, "accidents")
    fatal_latest = states[states.year == states.year.max()].nlargest(5, "fatalities")
    violation_latest = violations[violations.year == violations.year.max()].nlargest(3, "accidents")
    india_who = who[who.location == "India"]
    selected_names = ["India", "China", "Nepal", "Bangladesh", "Thailand",
                      "United States of America", "Australia", "Japan"]
    selected_who = who[who.location.isin(selected_names)].sort_values("death_rate_per_100k", ascending=False)
    summary = [
        "# RoadSafe Analytics — Project Findings",
        "",
        "## Scope and source caveats",
        "",
        "India state accident/fatality and traffic-rule figures are in the official Rajya Sabha answer. "
        "National injury totals are from the supplied MoRTH 2024 report; its public download URL was not independently confirmed. "
        "State/UT and traffic-rule records are from the official Rajya Sabha answer and annexes. "
        "The WHO source is indicator RS_198, an estimate per 100,000 population for 2021 only. "
        "These are separate analytical layers and are not directly comparable.",
        "",
        "## India national trends",
        "",
        f"In {int(end.year)}, the report records {int(end.accidents):,} accidents, "
        f"{int(end.fatalities):,} fatalities, and {int(end.persons_injured):,} injured persons. "
        f"For 2020-2024, reported accidents changed by "
        f"{(end.accidents / start.accidents - 1) * 100:.1f}% overall; this period includes the "
        "pandemic-affected 2020 observation, so the simple endpoint change needs context.",
        f"The 2024 fatality burden was {end.fatalities / end.accidents * 100:.1f} persons killed "
        "per 100 reported accidents. This ratio is not the percentage of accidents that were fatal, "
        "because an accident can involve multiple people and the report separately counts fatal accidents.",
        "",
        "## 2024 state/UT burden",
        "",
        "Highest observed accident counts:",
        "",
    ]
    summary.extend(f"- {row.state_ut}: {int(row.accidents):,}" for row in state_latest.itertuples())
    summary.extend([
        "",
        "Highest reported fatality counts:",
        "",
    ])
    summary.extend(f"- {row.state_ut}: {int(row.fatalities):,}" for row in fatal_latest.itertuples())
    summary.extend([
        "",
        "Counts measure reported burden, not exposure-adjusted risk. State population, traffic volume, "
        "vehicle-kilometers, and road length were not joined to this panel.",
        "",
        "## Reported traffic-rule categories",
        "",
        "The Ministry's Annexure II lists multiple categories. The highest accident counts in 2024 were:",
        "",
    ])
    summary.extend(f"- {row.category}: {int(row.accidents):,} accidents; {int(row.fatalities):,} fatalities"
                   for row in violation_latest.itertuples())
    summary.extend([
        "",
        "These administrative categories are not estimates of causal effects. Interpret the source's "
        "'Others' category cautiously.",
        "",
        "## Global mortality layer",
        "",
        f"The supplied WHO export contains {len(who)} location rows, all for 2021. "
        "Its rate is estimated road-traffic deaths per 100,000 population. It does not provide a "
        "multi-year series in this extract, and its estimates should not be interpreted as MoRTH counts.",
    ])
    if not india_who.empty:
        summary.append(f"The export's India value is {india_who.iloc[0].death_rate_per_100k} per 100,000 for 2021.")
    summary.extend([
        "Selected locations using the same WHO indicator and year:",
        "",
    ])
    summary.extend(f"- {row.location}: {row.death_rate_per_100k:.1f} per 100,000"
                   for row in selected_who.itertuples())
    summary.extend([
        "",
        "These comparisons are within one WHO estimate series; they are not comparisons with MoRTH's "
        "police-reported fatality counts.",
    ])
    summary.extend(["", "## Prediction experiment", ""])
    metrics_path = ROOT / "outputs/model_metrics.csv"
    if metrics_path.exists():
        metrics = pd.read_csv(metrics_path)
        for row in metrics.itertuples():
            summary.append(f"- {row.model}: MAE {row.mae:,.1f}; RMSE {row.rmse:,.1f}; R² {row.r2:.3f}.")
        summary.extend([
            "",
            "Evaluation trains on lagged state/UT records through 2023 and holds out 2024. "
            "There are only 36 state/UT test records and one held-out year, so these scores are "
            "illustrative and not reliable evidence of future performance.",
        ])
    else:
        summary.append("Run `python src/modeling.py` to generate time-aware holdout metrics; no score is asserted here.")
    summary.extend([
        "",
        "## Limitations and supported use",
        "",
        "Administrative reporting may undercount events and is subject to methods and coverage changes. "
        "The 2020 Jammu and Kashmir figure includes Ladakh while Ladakh is not separately reported that year. "
        "The processed source tables do not include a validated time-of-day field, so this project cannot "
        "answer which hour or time period has the most accidents. "
        "This short state panel supports a classroom forecasting demonstration, not a policy-grade forecast. "
        "Analyses describe associations and counts; they do not establish causes or prove that an intervention works.",
        "",
        "These findings may help prioritize follow-up analysis and guide questions about where reported burden "
        "is concentrated. Decisions on resources or enforcement require additional exposure, infrastructure, "
        "and local evidence.",
        "",
        "## Reproducibility",
        "",
        "See the repository README, `docs/DATA_SOURCES.md`, and `docs/DATA_DICTIONARY.md`. "
        "Regenerate this report with `python src/build_report.py` after running the cleaning and modeling workflow.",
        "",
        "## Sources",
        "",
        "- [MoRTH/Rajya Sabha Question 2172 answer and Annexures I-II](https://sansad.in/getFile/annex/270/AU2172_BvsIBX.pdf?source=pqars), answered 11 March 2026.",
        "- [WHO GHO indicator RS_198](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/estimated-road-traffic-death-rate-%28per-100-000-population%29).",
    ])
    output = ROOT / "reports/final_project_report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
