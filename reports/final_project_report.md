# RoadSafe Analytics — Project Findings

## Scope and source caveats

India state accident/fatality and traffic-rule figures are in the official Rajya Sabha answer. National injury totals are from the supplied MoRTH 2024 report; its public download URL was not independently confirmed. State/UT and traffic-rule records are from the official Rajya Sabha answer and annexes. The WHO source is indicator RS_198, an estimate per 100,000 population for 2021 only. These are separate analytical layers and are not directly comparable.

## India national trends

In 2024, the report records 487,707 accidents, 177,175 fatalities, and 471,441 injured persons. For 2020-2024, reported accidents changed by 31.0% overall; this period includes the pandemic-affected 2020 observation, so the simple endpoint change needs context.
The 2024 fatality burden was 36.3 persons killed per 100 reported accidents. This ratio is not the percentage of accidents that were fatal, because an accident can involve multiple people and the report separately counts fatal accidents.

## 2024 state/UT burden

Highest observed accident counts:

- Tamil Nadu: 67,526
- Madhya Pradesh: 56,669
- Kerala: 48,834
- Uttar Pradesh: 46,052
- Karnataka: 43,062

Highest reported fatality counts:

- Uttar Pradesh: 24,118
- Tamil Nadu: 18,449
- Maharashtra: 15,715
- Madhya Pradesh: 14,791
- Karnataka: 12,390

Counts measure reported burden, not exposure-adjusted risk. State population, traffic volume, vehicle-kilometers, and road length were not joined to this panel.

## Reported traffic-rule categories

The Ministry's Annexure II lists multiple categories. The highest accident counts in 2024 were:

- Over-speeding: 345,024 accidents; 124,522 fatalities
- Others: 105,389 accidents; 38,592 fatalities
- Driving on wrong side / lane indiscipline: 22,530 accidents; 8,327 fatalities

These administrative categories are not estimates of causal effects. Interpret the source's 'Others' category cautiously.

## Global mortality layer

The supplied WHO export contains 197 location rows, all for 2021. Its rate is estimated road-traffic deaths per 100,000 population. It does not provide a multi-year series in this extract, and its estimates should not be interpreted as MoRTH counts.
The export's India value is 14.6 per 100,000 for 2021.
Selected locations using the same WHO indicator and year:

- Nepal: 28.2 per 100,000
- Thailand: 25.4 per 100,000
- Bangladesh: 18.6 per 100,000
- China: 17.4 per 100,000
- India: 14.6 per 100,000
- United States of America: 14.2 per 100,000
- Australia: 4.5 per 100,000
- Japan: 2.7 per 100,000

These comparisons are within one WHO estimate series; they are not comparisons with MoRTH's police-reported fatality counts.

## Prediction experiment

- last_year_baseline: MAE 416.1; RMSE 734.2; R² 0.998.
- linear_regression: MAE 617.6; RMSE 1,055.7; R² 0.997.
- random_forest: MAE 1,110.1; RMSE 2,028.7; R² 0.987.

Evaluation trains on lagged state/UT records through 2023 and holds out 2024. There are only 36 state/UT test records and one held-out year, so these scores are illustrative and not reliable evidence of future performance.

## Limitations and supported use

Administrative reporting may undercount events and is subject to methods and coverage changes. The 2020 Jammu and Kashmir figure includes Ladakh while Ladakh is not separately reported that year. The processed source tables do not include a validated time-of-day field, so this project cannot answer which hour or time period has the most accidents. This short state panel supports a classroom forecasting demonstration, not a policy-grade forecast. Analyses describe associations and counts; they do not establish causes or prove that an intervention works.

These findings may help prioritize follow-up analysis and guide questions about where reported burden is concentrated. Decisions on resources or enforcement require additional exposure, infrastructure, and local evidence.

## Reproducibility

See the repository README, `docs/DATA_SOURCES.md`, and `docs/DATA_DICTIONARY.md`. Regenerate this report with `python src/build_report.py` after running the cleaning and modeling workflow.

## Sources

- [MoRTH/Rajya Sabha Question 2172 answer and Annexures I-II](https://sansad.in/getFile/annex/270/AU2172_BvsIBX.pdf?source=pqars), answered 11 March 2026.
- [WHO GHO indicator RS_198](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/estimated-road-traffic-death-rate-%28per-100-000-population%29).
