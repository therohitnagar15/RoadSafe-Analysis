USE roadsafe;

-- 1. GROUP BY: national trend and explicit per-accident measures.
SELECT year, accidents, fatalities, persons_injured,
       ROUND(fatalities / accidents * 100, 2) AS fatalities_per_100_accidents,
       ROUND(persons_injured / accidents * 100, 2) AS injuries_per_100_accidents
FROM india_national_year ORDER BY year;

-- 2. CASE and HAVING: group states by 2024 accident burden.
SELECT state_ut, accidents,
       CASE WHEN accidents >= 40000 THEN '40k+' 
            WHEN accidents >= 10000 THEN '10k-39,999'
            ELSE 'under 10k' END AS count_band
FROM india_state_accidents
WHERE year = 2024 AND accidents IS NOT NULL
HAVING accidents >= 10000
ORDER BY accidents DESC;

-- 3. Subquery: above the 2024 state/UT mean count.
SELECT state_ut, accidents
FROM india_state_accidents
WHERE year = 2024
  AND accidents > (SELECT AVG(accidents) FROM india_state_accidents WHERE year = 2024)
ORDER BY accidents DESC;

-- 3b. Highest reported fatality burden; counts are not exposure-adjusted risk.
SELECT state_ut, fatalities,
       ROUND(fatalities / NULLIF(accidents, 0) * 100, 2) AS fatalities_per_100_accidents
FROM india_state_accidents WHERE year = 2024
ORDER BY fatalities DESC LIMIT 10;

-- 3c. National traffic-rule violation categories, as recorded by the ministry.
SELECT category, accidents, fatalities,
       ROUND(fatalities / NULLIF(accidents, 0) * 100, 2) AS fatalities_per_100_accidents
FROM india_traffic_violations WHERE year = 2024
ORDER BY accidents DESC;

-- 4. CTE + window function: year-over-year state counts and rank.
WITH state_changes AS (
    SELECT state_ut, year, accidents,
           LAG(accidents) OVER (PARTITION BY state_ut ORDER BY year) AS prior_year
    FROM india_state_accidents
)
SELECT state_ut, year, accidents, prior_year,
       accidents - prior_year AS absolute_change,
       ROUND(100.0 * (accidents - prior_year) / NULLIF(prior_year, 0), 2) AS pct_change,
       DENSE_RANK() OVER (PARTITION BY year ORDER BY accidents DESC) AS rank_in_year
FROM state_changes ORDER BY year, rank_in_year;

-- 5. Global WHO layer: highest and lowest estimates, without joining to state records.
SELECT location, death_rate_per_100k, year
FROM who_road_death_rate
WHERE year = 2021 AND death_rate_per_100k IS NOT NULL
ORDER BY death_rate_per_100k DESC LIMIT 10;

-- 6. JOIN: compare model predictions to reported values for evaluation only.
SELECT p.state_ut, p.year, a.accidents AS reported_count,
       p.last_year_baseline, p.linear_regression, p.random_forest,
       ABS(a.accidents - p.last_year_baseline) AS baseline_absolute_error
FROM state_accident_prediction AS p
JOIN india_state_accidents AS a
  ON a.state_ut = p.state_ut AND a.year = p.year
ORDER BY baseline_absolute_error DESC;
