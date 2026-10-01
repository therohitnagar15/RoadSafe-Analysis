USE roadsafe;

-- Trailing three-year average: chronological state-level rolling summary.
WITH yearly AS (
    SELECT state_ut, year, accidents,
           AVG(accidents) OVER (
               PARTITION BY state_ut ORDER BY year
               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
           ) AS trailing_3yr_average
    FROM india_state_accidents
)
SELECT * FROM yearly ORDER BY state_ut, year;

-- Date analysis: report years are calendar years, represented as January 1.
SELECT STR_TO_DATE(CONCAT(year, '-01-01'), '%Y-%m-%d') AS report_year_date,
       SUM(accidents) AS state_accident_count
FROM india_state_accidents
GROUP BY year ORDER BY report_year_date;

-- CTE + HAVING: mean global rate by WHO parent region; distinct source layer.
WITH regional AS (
    SELECT w.parent_location AS who_region,
           AVG(w.death_rate_per_100k) AS mean_estimated_rate,
           COUNT(*) AS locations
    FROM who_road_death_rate AS w
    WHERE w.year = 2021 AND w.death_rate_per_100k IS NOT NULL
    GROUP BY w.parent_location
)
SELECT who_region, mean_estimated_rate, locations
FROM regional HAVING locations >= 5 ORDER BY mean_estimated_rate DESC;
