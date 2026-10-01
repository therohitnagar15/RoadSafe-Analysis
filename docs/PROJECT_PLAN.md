# RoadSafe Analytics — Phase 0 Project Plan

## Objective

Build a reproducible, explainable data science project that uses verified official road-safety data to describe accident and mortality patterns, examine recorded associations, and assess whether a defensible prediction task is supported.

## Why this project

Road safety is a consequential planning problem, and the analysis brings together core data science practices: source validation, relational storage and SQL, data quality, exploratory and time-aware analysis, visualization, and appropriately evaluated machine learning. The project is also designed to make methodological choices explainable in an academic and interview setting.

## Problem statement

Official road-safety observations may be spread across datasets with different definitions, units, years, and geographic coverage. The project will validate sources and preserve separate analytical layers where measures cannot be meaningfully joined. It will characterize observed patterns and report limitations rather than make causal or unsupported claims.

## Social and analytical objectives

- Summarize accident, fatality, and injury burden for the verified India accident source.
- Locate temporal and geographic variation supported by the actual fields.
- Examine recorded accident factors and outcomes as associations.
- Summarize country-level road-traffic mortality separately, if a suitable official global source is validated.
- Assess whether a prediction target has sufficient observations and valid time-aware evaluation.
- Present evidence that may inform further road-safety investigation and planning.

## Analytical questions

1. What are the observed year-wise patterns in accidents, fatalities, and injuries?
2. Which states/UTs or other geographic units have the highest counts and rates that the data can validly support?
3. How do fatality and injury measures vary across recorded categories and factors?
4. Which categories show changes over time, and how large are those changes?
5. How does country-level road-traffic mortality vary over time in the global source?
6. Can a non-leaky prediction problem be defined from the validated data, and how does a simple baseline perform?
7. Which conclusions are limited by coverage, reporting, definitions, or observational design?

## Scope decisions

- Keep India accident records and global country mortality as distinct analytical layers initially.
- Do not presume particular columns, years, units, row grain, or completeness.
- Distinguish total accident/fatality/injury counts, killed persons per accident, and deaths per population.
- Treat factor analyses as descriptive/associational unless a suitable causal design is independently justified.
- Attempt machine learning only after target, row grain, sample size, and leakage risks are understood.
- Do not represent model output as an intervention or promise of accident reduction.

## Dataset requirements for Phase 1

For each candidate dataset, verify and document: issuing organization, exact title, official source page/API/download endpoint, coverage, time range, observation grain, variable definitions, units, update cadence, missingness, duplicate behavior, known methodology, license/terms, and acquisition steps. Inspect the actual file before drafting its data dictionary or schema. Preserve original files as raw inputs.

## Success criteria

1. Provenance and license/attribution are recorded for every analyzed source.
2. A data dictionary reflects observed fields and definitions, not guessed columns.
3. Raw data is unchanged and all transformations can be reproduced.
4. MySQL tables and SQL analyses fit the source grain and include quality checks.
5. Metrics are clearly defined, denominators are explicit, and incomparable measures are not merged.
6. EDA answers stated questions, and charts identify units and periods.
7. Time-series validation respects chronology; leakage checks are documented.
8. Model selection and metrics match the target; a baseline is included when modeling is appropriate.
9. Insights are evidence-linked, qualified, and actionable only to the extent supported.
10. Setup, execution, limitations, and interview explanations are documented.

## Expected outputs

- Source register and data dictionary.
- Preserved raw data and reproducible processed data.
- MySQL schema, data-quality SQL, and analytical query scripts.
- Focused notebooks and reusable Python modules.
- Static and interactive visualizations where they add value.
- Model and evaluation artifacts only if justified by validated data.
- Final report, README, limitations, and interview preparation notes.

## Known and anticipated limitations

Specific limitations are unknown before source review. Items to investigate include under-reporting, administrative definition changes, missingness, differences in geographic granularity, population denominator alignment, estimates versus reported counts, and confounding. No result should be generalized beyond the data's population and period.

## README outline

1. Project title and status
2. Problem and objectives
3. Research questions
4. Data sources and definitions
5. Scope and layer comparability
6. Repository structure
7. Environment and setup
8. Database setup and data acquisition
9. Workflow and analysis
10. Results and visualizations
11. Model evaluation (if supported)
12. Limitations and responsible interpretation
13. Reproducibility
14. Acknowledgements, attribution, and licenses
15. Interview discussion guide

## Project execution status

The initial Phase 0 plan was reviewed and the user subsequently authorized completing the end-to-end project. Dataset validation and implementation proceeded under that instruction. Current source provenance and remaining validation limits are recorded in `DATA_SOURCES.md`; reproducible results are generated by the project scripts.
