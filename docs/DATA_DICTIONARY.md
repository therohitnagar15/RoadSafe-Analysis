# Data dictionary

The dictionary describes source fields used in this project. Nulls are retained where the source omits a value.

## `india_national_clean.csv`

| Column | Type | Definition |
|---|---|---|
| `year` | integer | Calendar year reported in MoRTH Table 1.1 (2020-2024) |
| `accidents` | integer | Total police-reported road accidents in India |
| `fatalities` | integer | Persons killed in reported road accidents |
| `persons_injured` | integer | Persons injured in reported road accidents |
| `fatalities_per_100_accidents` | float | Fatalities / accidents × 100; persons killed per 100 reported accidents, not percentage of accidents that were fatal |
| `injuries_per_100_accidents` | float | Persons injured / accidents × 100; may exceed 100 because an accident can injure multiple people |

## `india_state_accidents_clean.csv`

| Column | Type | Definition |
|---|---|---|
| `serial` | integer | State/UT sequence number in MoRTH Annexure I |
| `state_ut` | string | State/Union Territory label from the official table, with line breaks and J&K abbreviation normalized |
| `year` | integer | Calendar year 2020-2024 |
| `accidents` | integer/null | Reported state/UT accident count; null for source NA |
| `fatalities` | integer/null | Reported persons killed; null for source NA |
| `fatalities_per_100_accidents` | float/null | Fatalities / accidents × 100; persons killed per 100 reported accidents, not share of accidents that were fatal |
| `source_note` | string/null | Records the 2020 Jammu and Kashmir/Ladakh footnote, 2020 reconciliation of Tamil Nadu/West Bengal, and the source asterisk on Dadra & Nagar Haveli 2021-2022 values (the annex does not define the marker) |

## `india_traffic_violations_clean.csv`

| Column | Type | Definition |
|---|---|---|
| `category` | string | Category label from Rajya Sabha Q.2172 Annexure II |
| `year` | integer | Calendar year 2020-2024 |
| `accidents` | integer | Accidents reported under the national traffic-rule category |
| `fatalities` | integer | Fatalities reported under the national traffic-rule category |

These are ministry-reported categories, not causal effects. The report also identifies multiple contributing circumstances.

## `who_road_death_rate_clean.csv`

| Column | Type | Definition |
|---|---|---|
| `location_code` | string | WHO spatial code |
| `location` | string | WHO country/area label |
| `parent_location_code` | string | WHO parent region code |
| `parent_location` | string | WHO parent region label |
| `year` | integer | Source period; 2021 in supplied extract |
| `death_rate_per_100k` | float/null | WHO estimated road-traffic death rate per 100,000 population |
| `lower_estimate`, `upper_estimate` | float/null | Source uncertainty bounds; empty in this extract |
| `unit` | string/null | Source unit label |
| `modified_at` | string | Source modification timestamp |

## Model panel `india_state_model_features.csv`

Adds `previous_year_accidents`, grouped by state/UT with a one-year lag. The 2020 row is excluded because it has no preceding year in the report. A prior count is a forecast input only when it would be available at prediction time.

## Raw WHO columns

The original `data/raw/who_gho_rs_198.csv` preserves all 34 export columns. See WHO's indicator page for definitions and current source metadata; fields not used in the cleaned layer are not presumed to have a meaning beyond their source headers.
