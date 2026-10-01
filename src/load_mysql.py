"""Load processed CSVs into MySQL using credentials supplied via environment."""
from __future__ import annotations

import csv
import getpass
import os
from datetime import datetime
from pathlib import Path
import pymysql

ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)


def as_int(value):
    if value in (None, ""):
        return None
    try:
        # Convert to float first to strip the '.0', then convert to integer
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        return None  # Or return 0, depending on how you want to handle bad data



def as_float(value):
    return float(value) if value not in (None, "") else None


def main() -> None:
    required = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_DATABASE"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise EnvironmentError(f"Set database settings in environment: {', '.join(missing)}")
    password = os.getenv("MYSQL_PASSWORD") or getpass.getpass("MySQL password: ")
    connection = pymysql.connect(
        host=os.environ["MYSQL_HOST"], port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"], password=password,
        database=os.environ["MYSQL_DATABASE"], charset="utf8mb4", autocommit=False,
    )
    try:
        with connection.cursor() as cursor:
            for row in rows(ROOT / "data/processed/india_national_clean.csv"):
                cursor.execute(
                    """INSERT INTO india_national_year
                    (year, accidents, fatalities, persons_injured,
                     fatalities_per_100_accidents, injuries_per_100_accidents)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE accidents=VALUES(accidents),
                    fatalities=VALUES(fatalities), persons_injured=VALUES(persons_injured),
                    fatalities_per_100_accidents=VALUES(fatalities_per_100_accidents),
                    injuries_per_100_accidents=VALUES(injuries_per_100_accidents)""",
                    tuple(as_float(row[k]) if "per_100" in k else as_int(row[k])
                          for k in ["year", "accidents", "fatalities", "persons_injured",
                                    "fatalities_per_100_accidents", "injuries_per_100_accidents"]),
                )
            for row in rows(ROOT / "data/processed/india_state_accidents_clean.csv"):
                note = None
                if row["state_ut"] == "Jammu and Kashmir" and row["year"] == "2020":
                    note = "2020 figure includes Ladakh per report footnote"
                cursor.execute(
                    """INSERT INTO india_state_accidents
                    (state_ut,year,accidents,fatalities,fatalities_per_100_accidents,source_note)
                    VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
                    accidents=VALUES(accidents), fatalities=VALUES(fatalities),
                    fatalities_per_100_accidents=VALUES(fatalities_per_100_accidents),
                    source_note=VALUES(source_note)""",
                    (row["state_ut"], as_int(row["year"]), as_int(row["accidents"]),
                     as_int(row["fatalities"]), as_float(row["fatalities_per_100_accidents"]),
                     row["source_note"] or note),
                )
            for row in rows(ROOT / "data/processed/india_traffic_violations_clean.csv"):
                cursor.execute(
                    """INSERT INTO india_traffic_violations (category,year,accidents,fatalities)
                    VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
                    accidents=VALUES(accidents), fatalities=VALUES(fatalities)""",
                    (row["category"], as_int(row["year"]), as_int(row["accidents"]),
                     as_int(row["fatalities"])),
                )
            for row in rows(ROOT / "data/processed/who_road_death_rate_clean.csv"):
                modified = row["modified_at"] or None
                if modified:
                    modified = datetime.fromisoformat(modified.replace("Z", "+00:00")).replace(tzinfo=None)
                cursor.execute(
                    """INSERT INTO who_road_death_rate
                    (location_code,location,parent_location_code,parent_location,year,
                     death_rate_per_100k,lower_estimate,upper_estimate,unit,modified_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE location=VALUES(location),
                    death_rate_per_100k=VALUES(death_rate_per_100k),
                    lower_estimate=VALUES(lower_estimate), upper_estimate=VALUES(upper_estimate),
                    modified_at=VALUES(modified_at)""",
                    (row["location_code"], row["location"], row["parent_location_code"],
                     row["parent_location"], as_int(row["year"]),
                     as_float(row["death_rate_per_100k"]), as_float(row["lower_estimate"]),
                     as_float(row["upper_estimate"]), row["unit"] or None, modified),
                )
            predictions = ROOT / "outputs/2024_state_predictions.csv"
            if predictions.exists():
                for row in rows(predictions):
                    cursor.execute(
                        """INSERT INTO state_accident_prediction
                        (state_ut,year,actual_accidents,last_year_baseline,
                         linear_regression,random_forest) VALUES (%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE actual_accidents=VALUES(actual_accidents),
                        last_year_baseline=VALUES(last_year_baseline),
                        linear_regression=VALUES(linear_regression),
                        random_forest=VALUES(random_forest)""",
                        (row["state_ut"], as_int(row["year"]),
                         as_int(row["actual_accidents"]), as_float(row["last_year_baseline"]),
                         as_float(row["linear_regression"]), as_float(row["random_forest"])),
                    )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    print("MySQL load completed.")


if __name__ == "__main__":
    main()
