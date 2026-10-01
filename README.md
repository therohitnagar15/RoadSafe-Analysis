# RoadSafe Analytics

**Road Accident Risk & Fatality Intelligence System**

RoadSafe Analytics examines reported road accidents in India and estimated road-traffic death rates internationally. It demonstrates source validation, SQL/MySQL, Python data preparation, exploratory analysis, visualization, and a carefully scoped time-aware prediction exercise.

> **Evidence note:** State-level accident/fatality counts and national traffic-rule categories come from a 2026 official Rajya Sabha answer by MoRTH (linked in the source register). National injury totals come from the supplied *Road Accidents in India 2024* report; its exact public download URL could not be independently confirmed, though its accident/fatality totals reconcile to the official answer. The WHO extract has only 2021 observations. All conclusions below are descriptive; rates and sources are not interchangeable.

## Project questions

- How did India's reported accident, fatality, and injury totals vary during 2020-2024?
- Which states/UTs had the largest reported accident counts in 2024, and how did counts vary over the five reported years?
- How many persons were killed per 100 reported accidents at national level?
- How did WHO's 2021 country/area estimated road-traffic death rate vary across its locations?
- How does India compare with selected locations using that same WHO indicator and year?
- How does a last-year baseline compare with simple regressors on a 2024 state-count holdout?

The final question is a small educational forecast experiment, not a validated operational risk model. The project does not claim that the model reduces accidents or that a state count measures individual risk.

## Data layers

1. **India police-reported accident layer:** MoRTH/TRW data for calendar years 2020-2024, including official Rajya Sabha Annexures with state/UT accidents and fatalities and national traffic-rule categories. The supplied 2024 report adds national accidents, fatalities, and injuries. Ladakh is unavailable in 2020; the report notes Jammu and Kashmir includes Ladakh that year.
2. **Global mortality layer:** WHO GHO indicator RS_198, estimated road-traffic deaths per 100,000 population, one year (2021) across 197 locations in the supplied export.

These sources have different concepts and methods. No join or direct rank comparison between India's accident counts and WHO mortality estimates is used. Definitions, source checks, limitations, and the detailed data dictionary are in [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) and [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md).

## Repository map

```text
data/raw/          Preserved WHO CSV and supplied MoRTH PDF
data/processed/    Reproducible extracted and cleaned CSVs (created by scripts)
notebooks/         Six learning notebooks, one for each main analysis stage
sql/               MySQL schema, imports/quality checks, and analytical queries
src/               Collection, cleaning, features, visualization, model, SQL loader
outputs/            Metrics, predictions, charts, and final report
reports/            Source extraction text and report documentation
docs/               Source register, data dictionary, project plan
```

## Environment setup

Python 3.13 and MySQL 8.0+ are the verified target. The requirements file pins the library versions used to generate the included outputs. PDF extraction uses `pdfplumber` for the parliamentary annex and Poppler's `pdftotext` for the supplied report, so `pdftotext` must be on `PATH`. Create and activate an isolated environment, then install:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Optional, only if JupyterLab is not already installed:
python -m pip install -r requirements-notebooks.txt
```

For a Unix-like shell, activate with `source .venv/bin/activate`.

## Reproduce the workflow

Run from the repository root:

```powershell
python src/data_collection.py
python src/data_cleaning.py
python src/data_quality_report.py
python src/feature_engineering.py
python src/visualization.py
python src/modeling.py
python src/build_report.py
```

The extraction script reads the preserved PDFs, validates table row counts and checks state totals/category totals against national figures for 2020-2024. The cleaning step keeps the India and WHO layers separate, validates keys and nonnegative values, and computes explicitly named per-accident metrics. The feature step uses only the preceding year's count. The modeling script trains on outcomes through 2023 and evaluates the 2024 state/UT holdout; it reports a last-year baseline, linear regression, and random forest using MAE, RMSE, and R², and saves the fitted pipelines. See `outputs/model_evaluation.json` for the limitations of that holdout. The report generator summarizes the resulting source-backed outputs.

Run notebooks in order with Jupyter:

```powershell
jupyter lab
```

## MySQL setup

1. Create the database/tables by executing [`sql/schema.sql`](sql/schema.sql) in MySQL 8.
2. Run the CSV workflow above so `data/processed/` contains cleaned files.
3. Set `MYSQL_HOST`, `MYSQL_PORT` (optional), `MYSQL_USER`, and `MYSQL_DATABASE` in the process environment. The loader securely prompts for the password unless `MYSQL_PASSWORD` is already set. Never put credentials in source files.
4. Run `python src/load_mysql.py`.
5. Execute `sql/data_quality.sql`, `sql/analysis_queries.sql`, and `sql/advanced_analysis.sql`.

The SQL uses `GROUP BY`, `HAVING`, `CASE`, joins, subqueries, CTEs, window functions, and date handling. If model predictions exist, the loader imports them into a separate evaluation table; prediction results never replace source counts.

## Outputs

- `data/processed/india_national_clean.csv`
- `data/processed/india_state_accidents_clean.csv`
- `data/processed/india_traffic_violations_clean.csv`
- `data/processed/who_road_death_rate_clean.csv`
- `outputs/figures/` static PNGs and interactive Plotly HTML files
- `outputs/model_metrics.csv` and `outputs/2024_state_predictions.csv`
- `outputs/model_interpretation.csv` and serialized pipelines in `models/`
- `reports/final_project_report.md`
- `reports/data_quality_summary.md`

Model scores are generated by running the pipeline in the declared environment. The state panel has only five calendar years, only 36 state/UT units, and one test year, so model results are illustrative and highly uncertain. WHO's one-year extract does not support trend or forecasting claims.

## Interpretation and limitations

- `fatalities / accidents × 100` means **persons killed per 100 reported accidents**, not the percentage of accidents that were fatal.
- Deaths per 100,000 population are a separate population-normalized WHO estimate.
- Reported counts depend on administrative collection and the report's definitions. Observed associations are not causal evidence.
- Population, exposure, road length, traffic volume, and vehicle-kilometers are not aligned here for state-level risk normalization.
- The extracted tables do not provide a validated hour-of-day field, so time-of-day patterns are outside this build.
- State boundaries/reporting coverage and the Jammu and Kashmir/Ladakh 2020 note limit comparisons.
- The machine-learning evaluation has only a single held-out year. It is insufficient for strong generalization claims.

## Sources and attribution

- Ministry of Road Transport and Highways / Transport Research Wing, *Road Accidents in India 2024* (supplied source copy); national totals are corroborated by the linked official Lok Sabha answer in [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).
- World Health Organization, Global Health Observatory indicator RS_198. See the WHO links in [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

No explicit reuse license was present in the supplied report. Check the applicable source terms before redistribution. Project code/documentation license: not selected.
