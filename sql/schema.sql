CREATE DATABASE IF NOT EXISTS roadsafe
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE roadsafe;

CREATE TABLE IF NOT EXISTS india_national_year (
    year SMALLINT NOT NULL,
    accidents INT UNSIGNED NOT NULL,
    fatalities INT UNSIGNED NOT NULL,
    persons_injured INT UNSIGNED NOT NULL,
    fatalities_per_100_accidents DECIMAL(8,3) NOT NULL,
    injuries_per_100_accidents DECIMAL(8,3) NOT NULL,
    PRIMARY KEY (year),
    CHECK (year BETWEEN 1900 AND 2100)
);

CREATE TABLE IF NOT EXISTS india_state_accidents (
    state_ut VARCHAR(100) NOT NULL,
    year SMALLINT NOT NULL,
    accidents INT UNSIGNED NULL,
    fatalities INT UNSIGNED NULL,
    fatalities_per_100_accidents DECIMAL(8,3) NULL,
    source_note VARCHAR(255) NULL,
    PRIMARY KEY (state_ut, year),
    INDEX idx_state_year (year, state_ut),
    CHECK (year BETWEEN 1900 AND 2100)
);

CREATE TABLE IF NOT EXISTS india_traffic_violations (
    category VARCHAR(120) NOT NULL,
    year SMALLINT NOT NULL,
    accidents INT UNSIGNED NOT NULL,
    fatalities INT UNSIGNED NOT NULL,
    PRIMARY KEY (category, year),
    INDEX idx_violation_year (year, category)
);

CREATE TABLE IF NOT EXISTS who_road_death_rate (
    location_code CHAR(3) NOT NULL,
    location VARCHAR(150) NOT NULL,
    parent_location_code VARCHAR(12) NULL,
    parent_location VARCHAR(100) NULL,
    year SMALLINT NOT NULL,
    death_rate_per_100k DECIMAL(10,4) NULL,
    lower_estimate DECIMAL(10,4) NULL,
    upper_estimate DECIMAL(10,4) NULL,
    unit VARCHAR(50) NULL,
    modified_at DATETIME NULL,
    PRIMARY KEY (location_code, year),
    INDEX idx_who_year_rate (year, death_rate_per_100k)
);

CREATE TABLE IF NOT EXISTS state_accident_prediction (
    state_ut VARCHAR(100) NOT NULL,
    year SMALLINT NOT NULL,
    actual_accidents INT UNSIGNED NOT NULL,
    last_year_baseline DECIMAL(12,3) NOT NULL,
    linear_regression DECIMAL(12,3) NOT NULL,
    random_forest DECIMAL(12,3) NOT NULL,
    PRIMARY KEY (state_ut, year),
    INDEX idx_prediction_year (year)
);
