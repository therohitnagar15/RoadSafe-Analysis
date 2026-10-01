# Data quality and source inspection

Generated from the preserved inputs and processed tables. This is a structural quality review, not a claim that source reporting is complete.

## Raw WHO export

- Shape: 197 rows × 34 columns
- Duplicate complete rows: 0
- Duplicate `SpatialDimValueCode, Period` keys: 0
- Date/time-like columns by name: DateModified
- Numeric columns: Period, Dim1 type, Dim1, Dim1ValueCode, Dim2 type, Dim2, Dim2ValueCode, Dim3 type, Dim3, Dim3ValueCode, DataSourceDimValueCode, DataSource, FactValueNumericPrefix, FactValueNumeric, FactValueUoM, FactValueNumericLowPrefix, FactValueNumericLow, FactValueNumericHighPrefix, FactValueNumericHigh, Value, FactValueTranslationID, FactComments
- Categorical/text columns: IndicatorCode, Indicator, ValueType, ParentLocationCode, ParentLocation, Location type, SpatialDimValueCode, Location, Period type, IsLatestYear, Language, DateModified
- Column data types:

```text
IndicatorCode                     str
Indicator                         str
ValueType                         str
ParentLocationCode                str
ParentLocation                    str
Location type                     str
SpatialDimValueCode               str
Location                          str
Period type                       str
Period                          int64
IsLatestYear                     bool
Dim1 type                     float64
Dim1                          float64
Dim1ValueCode                 float64
Dim2 type                     float64
Dim2                          float64
Dim2ValueCode                 float64
Dim3 type                     float64
Dim3                          float64
Dim3ValueCode                 float64
DataSourceDimValueCode        float64
DataSource                    float64
FactValueNumericPrefix        float64
FactValueNumeric              float64
FactValueUoM                  float64
FactValueNumericLowPrefix     float64
FactValueNumericLow           float64
FactValueNumericHighPrefix    float64
FactValueNumericHigh          float64
Value                         float64
FactValueTranslationID        float64
FactComments                  float64
Language                          str
DateModified                      str
```
- Columns with missing values:

  - `Dim1 type`: 197
  - `Dim1`: 197
  - `Dim1ValueCode`: 197
  - `Dim2 type`: 197
  - `Dim2`: 197
  - `Dim2ValueCode`: 197
  - `Dim3 type`: 197
  - `Dim3`: 197
  - `Dim3ValueCode`: 197
  - `DataSourceDimValueCode`: 197
  - `DataSource`: 197
  - `FactValueNumericPrefix`: 197
  - `FactValueUoM`: 197
  - `FactValueNumericLowPrefix`: 197
  - `FactValueNumericLow`: 197
  - `FactValueNumericHighPrefix`: 197
  - `FactValueNumericHigh`: 197
  - `FactValueTranslationID`: 197
  - `FactComments`: 197

- Indicator codes: RS_198
- Indicator labels: Estimated road traffic death rate (per 100 000 population)
- Periods: 2021
- Locations: 197
- DateModified values: 2024-04-14T18:30:00.000Z
- Data type grouping follows observed file types; `Period` is numeric-looking text in the raw export and is converted to integer in the cleaned layer.

## Clean India national annual table

- Shape: 5 rows × 6 columns
- Duplicate complete rows: 0
- Duplicate `year` keys: 0
- Date/time-like columns by name: none
- Numeric columns: year, accidents, fatalities, persons_injured, fatalities_per_100_accidents, injuries_per_100_accidents
- Categorical/text columns: none
- Column data types:

```text
year                              int64
accidents                         int64
fatalities                        int64
persons_injured                   int64
fatalities_per_100_accidents    float64
injuries_per_100_accidents      float64
```
- Columns with missing values:

  - None

## Clean India state/UT annual panel

- Shape: 180 rows × 7 columns
- Duplicate complete rows: 0
- Duplicate `state_ut, year` keys: 0
- Date/time-like columns by name: none
- Numeric columns: serial, year, accidents, fatalities, fatalities_per_100_accidents
- Categorical/text columns: state_ut, source_note
- Column data types:

```text
serial                            int64
state_ut                            str
year                              int64
accidents                       float64
fatalities                      float64
source_note                         str
fatalities_per_100_accidents    float64
```
- Columns with missing values:

  - `accidents`: 1
  - `fatalities`: 1
  - `source_note`: 172
  - `fatalities_per_100_accidents`: 2

## Clean India traffic-rule categories

- Shape: 30 rows × 4 columns
- Duplicate complete rows: 0
- Duplicate `category, year` keys: 0
- Date/time-like columns by name: none
- Numeric columns: year, accidents, fatalities
- Categorical/text columns: category
- Column data types:

```text
category        str
year          int64
accidents     int64
fatalities    int64
```
- Columns with missing values:

  - None

## Clean WHO country/area panel

- Shape: 197 rows × 10 columns
- Duplicate complete rows: 0
- Duplicate `location_code, year` keys: 0
- Date/time-like columns by name: none
- Numeric columns: year, death_rate_per_100k, lower_estimate, upper_estimate, unit
- Categorical/text columns: location_code, location, parent_location_code, parent_location, modified_at
- Column data types:

```text
location_code               str
location                    str
parent_location_code        str
parent_location             str
year                      int64
death_rate_per_100k     float64
lower_estimate          float64
upper_estimate          float64
unit                    float64
modified_at                 str
```
- Columns with missing values:

  - `lower_estimate`: 197
  - `upper_estimate`: 197
  - `unit`: 197

## Cleaning decisions

- WHO interval-bound fields are empty in the supplied CSV and remain null; no confidence bounds are invented.
- WHO source disaggregation fields are empty; the analysis uses the documented indicator-level numeric fact.
- Zero values are retained as source values and are not changed into missing values.
- The 2020 Ladakh NA remains null. The 2020 Jammu and Kashmir footnote is stored in `source_note`.
- Source asterisks on Dadra & Nagar Haveli's 2021-2022 observations are retained as a note; the annex does not explain them.
- State and national totals and traffic-rule category totals reconcile for accidents and fatalities in each year 2020-2024.
- No source file was overwritten; derived files are written under `data/processed/`.

