# Data source register and validation notes

Validation reviewed: 2026-10-01. The raw files supplied with the project were preserved in `data/raw/`.

## India accident layer

| Field | Detail |
|---|---|
| Organization/title | Government of India, Ministry of Road Transport and Highways (MoRTH), Rajya Sabha Unstarred Question 2172 answer (11 March 2026), Annexures I-II; plus *Road Accidents in India 2024* (supplied PDF) |
| Coverage | India states and Union Territories; report tables cover calendar years 2020-2024 |
| Acquisition | Official 5-page parliamentary PDF downloaded to `data/raw/morth_parliament_annex_2026.pdf`; `src/data_collection.py` extracts its digital tables with `pdfplumber`. National accidents/fatalities/injuries also use Table 1.1 from the supplied report and are reconciled against official annex totals. |
| Provenance check | The parliamentary answer states that state/UT data came from States/UTs and covers all road categories. Annexure I contains state/UT accidents and fatalities; Annexure II contains nationwide traffic-rule category totals. The supplied report identifies MoRTH/TRW and police collection using UNESCAP/APRAD standardized formats. The exact public download URL for the supplied 2024 report could not be independently confirmed; its national accident/fatality totals reconcile to the official parliamentary source, while injury totals are taken from the supplied report. |
| Main fields | National year, accidents, fatalities, persons injured; state/UT-year accident and fatality counts; national traffic-rule-category counts |
| Units | Counts of reported accidents/persons |
| Missingness | Annexure I reports Ladakh as NA for accidents and fatalities in 2020. The supplied report says Jammu and Kashmir includes Ladakh in 2020. Do not compare these two units separately for that year. Annexure I marks Dadra & Nagar Haveli's 2021-2022 cells with an asterisk but gives no key for it. |
| License/terms | No explicit license statement was found in the supplied report. Attribute MoRTH/TRW and check the publication's reuse terms before redistribution. |
| Caveat | Administrative reports reflect police-reported counts and may not equal modeled international mortality estimates. |

Official source: [Rajya Sabha Q.2172 answer and MoRTH Annexures I-II](https://sansad.in/getFile/annex/270/AU2172_BvsIBX.pdf?source=pqars). The [Lok Sabha reply containing 2020-2024 accident totals](https://sansad.in/getFile/loksabhaquestions/annex/187/AU2259_hBNj9R.pdf?source=pqals) corroborates national totals. MoRTH publication search: [Road Accidents in India](https://morth.nic.in/search/node/road%20accidents).

## Global mortality layer

| Field | Detail |
|---|---|
| Organization/title | World Health Organization, Global Health Observatory indicator RS_198, *Estimated road traffic death rate (per 100 000 population)* |
| Coverage | 197 country/area location records in the supplied export, all for year 2021 |
| Acquisition | Supplied CSV export. WHO's legacy GHO endpoint is retired; WHO currently documents the World Health Data Hub and indicator pages. Download/export the indicator CSV from its current WHO page and record the download date and metadata; do not use the retired Athena API. |
| Indicator definition | Estimated road traffic fatal-injury deaths per 100,000 population; an estimate rather than the MoRTH police-reported accident count. WHO describes differing estimation methods by country data group and notes collection is not annual. |
| Fields and units | Value is deaths per 100,000 population; low/high estimate fields are present but entirely empty in this export. |
| Missingness | 197 rows, 34 source columns. Disaggregation columns are empty in this extract; numerical low/high bounds also empty. The `Value` string and numeric fact field are both supplied; analysis uses `FactValueNumeric`. Four numeric zeros are retained and not silently reinterpreted. |
| Updated | Source CSV records `DateModified=2024-04-14T18:30:00.000Z`. WHO metadata says this methodology is not collected every year. The extract's period is only 2021. |
| License/terms | Preserve WHO attribution. The supplied CSV has no recorded reuse license; review WHO terms before redistribution. |
| Caveat | Not directly interchangeable with MoRTH's reported deaths or accidents: definitions, methods, and population denominators differ. This one-year file is cross-sectional, not a trend series. |

Official pages: [WHO indicator details](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/estimated-road-traffic-death-rate-%28per-100-000-population%29), [WHO GHO OData/API status and current data access](https://www.who.int/data/gho/info/gho-odata-api), and [WHO road traffic deaths topic page](https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/road-traffic-deaths).

## Revalidation policy

Before replacing either source, check that the indicator code/title, reference period, definitions, geography, units, missingness, update date, and license still match. Compare the new file's schema to the current scripts. Do not silently append WHO and MoRTH rates into one series.
