# Interview preparation

## Project summary

I built RoadSafe Analytics to explore official road-safety observations while respecting differences between police-reported accident counts and WHO's estimated population-normalized road-traffic mortality. The workflow extracts and validates source tables, cleans data with pandas/NumPy, stores separate layers in MySQL, analyzes changes with SQL and Python, visualizes counts/rates, and compares a simple lag-based regression against a carry-forward baseline using a chronological 2024 holdout.

## Common questions and grounded answers

**Why this project?** Road safety is a meaningful public planning problem and it uses practical skills from ingestion through interpretation. It also lets me demonstrate careful source validation and clear communication of limitations.

**Why these sources?** MoRTH/TRW supplies India police-reported accident tables and WHO supplies a country-level estimated death rate. They answer different questions and are kept as separate layers. The supplied MoRTH report's exact public download URL needs confirmation even though an official Lok Sabha reply corroborates its national totals.

**Why SQL/MySQL?** A relational database gives explicit schemas, keys, indexes, quality queries, and reusable aggregations. SQL CTEs make multi-step logic readable, and window functions compare a state with its prior year without self-joins.

**Why Pandas and NumPy?** Pandas handles tabular typing, null-aware grouping, joins, and time ordering. NumPy supports numerical operations such as RMSE; vectorized operations avoid brittle row-by-row loops.

**Why Matplotlib, Seaborn, and Plotly?** Matplotlib gives a controlled static time-series chart; Seaborn provides readable distribution summaries; Plotly adds hover and geographic interaction where it helps compare countries and states.

**Why these models?** The modeling target is numeric state/UT accident count. A last-year baseline is essential. Linear regression provides a simple interpretable comparison; random forest checks whether nonlinear patterns improve the error. The panel is small, so neither should be treated as a robust forecasting system.

**Why MAE/RMSE/R²?** MAE is the typical absolute error in accident-count units. RMSE penalizes larger misses more strongly. R² gives a reference against a mean-only predictor but can be negative on a weak holdout; no single metric is sufficient.

**How was leakage prevented?** The prior-year count is made with a within-state `shift(1)`. Training outcomes end in 2023; every 2024 record is held out. No random split mixes later years into training.

**How were missing values handled?** Ladakh 2020 remains null. Jammu and Kashmir's 2020 count has a source note saying it includes Ladakh. WHO's empty interval bounds remain null. No missing observations are filled with invented values.

**Biggest data challenge?** The MoRTH report is a PDF with wrapped table labels, separate serial lines, and a footnote affecting geographic comparability. The extractor checks expected row counts and preserves the exceptional 2020 note.

**What are the limitations?** A short five-year administrative panel, one forecast test year, no exposure denominator for state comparisons, reporting/coverage differences, and non-comparable WHO and MoRTH definitions.

**What did I learn?** Source provenance and row grain determine what can be analyzed. A good baseline and honest holdout often matter more than adding algorithms. Clear rates require clear denominators.

## Important interview phrasing

Say “associated with” for observational relationships; do not claim causation. Describe state counts as burden, not per-person risk. State that the model is a small educational forecast experiment and cannot establish policy impact.
