USE roadsafe;

-- Primary keys prevent duplicate year / state-year / location-year records.
SELECT 'national_rows' AS check_name, COUNT(*) AS result
FROM india_national_year;

SELECT 'state_year_duplicate_groups' AS check_name, COUNT(*) AS result
FROM (
    SELECT state_ut, year FROM india_state_accidents
    GROUP BY state_ut, year HAVING COUNT(*) > 1
) AS duplicates;

SELECT 'negative_or_missing_accident_counts' AS check_name, COUNT(*) AS result
FROM india_state_accidents
WHERE accidents < 0 OR (accidents IS NULL AND year <> 2020);

SELECT 'fatalities_over_accidents_review' AS check_name, COUNT(*) AS result
FROM india_state_accidents WHERE fatalities > accidents;

-- Source table totals should reconcile by year. 2020 includes footnote caveat:
-- Jammu & Kashmir includes Ladakh, while Ladakh is unavailable separately.
WITH state_totals AS (
    SELECT year, SUM(accidents) AS state_sum
    FROM india_state_accidents GROUP BY year
)
SELECT n.year, n.accidents AS national_total, s.state_sum,
       s.state_sum - n.accidents AS difference
FROM india_national_year AS n
JOIN state_totals AS s ON s.year = n.year;

SELECT location_code, year, death_rate_per_100k
FROM who_road_death_rate
WHERE death_rate_per_100k < 0;
