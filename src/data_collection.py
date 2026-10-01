"""Extract reproducible analytical inputs from the supplied official reports."""
from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data" / "raw" / "morth_road_accidents_india_2024.pdf"
PARLIAMENT_REPORT = ROOT / "data" / "raw" / "morth_parliament_annex_2026.pdf"
OUTPUT = ROOT / "data" / "processed"
YEARS = (2020, 2021, 2022, 2023, 2024)


def report_text(path: Path = REPORT) -> str:
    """Extract selectable PDF text using Poppler's pdftotext utility."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        # The supplied PDF's selectable text includes Windows-1252 punctuation.
        encoding="cp1252",
    )
    return result.stdout


def number(value: str) -> int | None:
    normalized = re.sub(r"\s+", "", value).rstrip("*")
    return None if normalized.upper() == "NA" else int(normalized.replace(",", ""))


def extract_national_trends(text: str) -> list[dict[str, int]]:
    start = text.rfind("Table 1.1:")
    section = text[start:].split("Chart 1.1:", 1)[0]
    rows = []
    pattern = re.compile(
        r"(?m)^\s*(2020|2021|2022|2023|2024)\s+([\d,]+)\s+"
        r"(?:-?[\d.]+)?\s+([\d,]+)\s+(?:-?[\d.]+)?\s+([\d,]+)"
    )
    for year, accidents, fatalities, injuries in pattern.findall(section):
        rows.append({
            "year": int(year),
            "accidents": int(accidents.replace(",", "")),
            "fatalities": int(fatalities.replace(",", "")),
            "persons_injured": int(injuries.replace(",", "")),
        })
    if len(rows) != 5:
        raise ValueError(f"Expected five Table 1.1 year rows; extracted {len(rows)}")
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def find_pdf_table(path: Path, marker: str) -> list[list[str | None]]:
    """Find a selectable PDF table by a distinctive title on its page."""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if marker.casefold() in page_text.casefold():
                tables = page.extract_tables()
                if tables:
                    return max(tables, key=len)
    raise ValueError(f"Could not find a table for {marker!r} in {path.name}")


def extract_state_panel(table: list[list[str | None]]) -> list[dict[str, object]]:
    """Read the official 2026 parliamentary table with accidents and fatalities."""
    rows = []
    for cells in table:
        if len(cells) < 12 or not cells[0] or not cells[0].strip().isdigit():
            continue
        serial, name = int(cells[0].strip()), " ".join((cells[1] or "").split())
        values = [cell or "" for cell in cells[2:12]]
        if not name or len(values) != 10:
            continue
        if serial == 33:
            name = "Jammu and Kashmir"
        note = None
        if any(value.endswith("*") for value in values):
            note = "Source marks 2021/2022 cells with an asterisk; no key is given in Annexure I"
        for index, year in enumerate(YEARS):
            accident_token, fatality_token = values[index * 2:index * 2 + 2]
            row_note = note
            if serial == 33 and year == 2020:
                row_note = "Supplied MoRTH table footnote says this 2020 Jammu and Kashmir value includes Ladakh"
            if serial in (23, 28) and year == 2020:
                row_note = "Rajya Sabha Annexure I footnote: data reconciled for Tamil Nadu and West Bengal in 2020"
            rows.append({
                "serial": serial,
                "state_ut": name,
                "year": year,
                "accidents": number(accident_token.rstrip("*")),
                "fatalities": number(fatality_token.rstrip("*")),
                "source_note": row_note,
            })
    state_count = len({row["serial"] for row in rows})
    if state_count != 36 or len(rows) != 180:
        raise ValueError(f"Expected 36 x 5 official state/UT rows, found {state_count} and {len(rows)}")
    return rows


def extract_traffic_violations(table: list[list[str | None]]) -> list[dict[str, object]]:
    """Read the official national traffic-rule category table (not causal effects)."""
    rows = []
    for cells in table:
        if len(cells) < 11 or not cells[0]:
            continue
        category = " ".join(cells[0].split())
        category = category.replace("consump tion", "consumption").replace("lan e", "lane")
        if category.casefold() in {"categories", "total"}:
            continue
        values = [cell or "" for cell in cells[1:11]]
        if len(values) != 10:
            continue
        for index, year in enumerate(YEARS):
            rows.append({
                "category": category,
                "year": year,
                "accidents": number(values[index * 2]),
                "fatalities": number(values[index * 2 + 1]),
            })
    if len(rows) != 30:
        raise ValueError(f"Expected 6 traffic-rule categories x 5 years, got {len(rows)}")
    return rows


def main() -> None:
    text = report_text()
    state_table = find_pdf_table(PARLIAMENT_REPORT, "State-wise number of Road Accidents and Fatalities")
    violation_table = find_pdf_table(PARLIAMENT_REPORT, "Details of Road Accidents and Fatalities due to Traffic Rule Violations")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    national = extract_national_trends(text)
    states = extract_state_panel(state_table)
    violations = extract_traffic_violations(violation_table)
    national_by_year = {row["year"]: row for row in national}
    for year in YEARS:
        state_rows = [row for row in states if row["year"] == year]
        violation_rows = [row for row in violations if row["year"] == year]
        state_accidents = sum(row["accidents"] or 0 for row in state_rows)
        state_fatalities = sum(row["fatalities"] or 0 for row in state_rows)
        violation_accidents = sum(row["accidents"] for row in violation_rows)
        violation_fatalities = sum(row["fatalities"] for row in violation_rows)
        expected = national_by_year[year]
        if (state_accidents, state_fatalities) != (expected["accidents"], expected["fatalities"]):
            raise ValueError(f"State panel does not reconcile to national totals for {year}")
        if (violation_accidents, violation_fatalities) != (expected["accidents"], expected["fatalities"]):
            raise ValueError(f"Traffic-rule categories do not reconcile to national totals for {year}")
    write_csv(OUTPUT / "india_national_trends.csv", national,
              ["year", "accidents", "fatalities", "persons_injured"])
    write_csv(OUTPUT / "india_state_accidents.csv", states,
              ["serial", "state_ut", "year", "accidents", "fatalities", "source_note"])
    write_csv(OUTPUT / "india_traffic_violations.csv", violations,
              ["category", "year", "accidents", "fatalities"])
    wide = []
    for serial in sorted({int(row["serial"]) for row in states}):
        group = [row for row in states if int(row["serial"]) == serial]
        record: dict[str, object] = {"serial": serial, "state_ut": group[0]["state_ut"]}
        for row in group:
            record[f"accidents_{row['year']}"] = row["accidents"]
            record[f"fatalities_{row['year']}"] = row["fatalities"]
        wide.append(record)
    write_csv(OUTPUT / "india_state_accidents_wide.csv", wide,
              ["serial", "state_ut", *[f"{m}_{y}" for y in YEARS
                                        for m in ("accidents", "fatalities")]])
    print(f"Extracted {len(national)} national rows and {len(states)} state/UT-year rows.")
    print("State and traffic-rule accident/fatality totals reconcile for 2020-2024.")
    print(f"Wrote reproducible CSVs to {OUTPUT}")


if __name__ == "__main__":
    main()
