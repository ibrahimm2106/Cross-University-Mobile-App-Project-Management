#!/usr/bin/env python3
"""Lightweight consistency checks for the portfolio repository."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_gantt() -> None:
    rows = read_csv("data/gantt_schedule.csv")
    assert len(rows) == 30, f"Expected 30 Gantt tasks, found {len(rows)}"

    for row in rows:
        start = datetime.strptime(row["Start Date"], "%d-%b-%Y")
        end = datetime.strptime(row["End Date"], "%d-%b-%Y")
        assert start <= end, f"Invalid date range for {row['Task Name']}"
        assert int(row["Duration (weeks)"]) > 0, f"Invalid duration for {row['Task Name']}"

    assert rows[0]["Start Date"] == "01-Sep-2025"
    assert rows[-1]["End Date"] == "23-Feb-2026"


def validate_budget() -> None:
    rows = read_csv("data/budget.csv")
    total_rows = [row for row in rows if row["Budget Item"] == "TOTAL"]
    assert len(total_rows) == 1, "Budget must contain exactly one TOTAL row"
    assert int(total_rows[0]["Amount GBP"]) == 22550, "PID total must be £22,550"

    component_total = sum(
        int(row["Amount GBP"])
        for row in rows
        if row["Budget Item"] != "TOTAL"
    )
    assert component_total == 22550, f"Budget components total £{component_total:,}, expected £22,550"


def validate_stakeholders() -> None:
    rows = read_csv("data/stakeholders.csv")
    assert len(rows) == 12, f"Expected 12 stakeholder groups, found {len(rows)}"
    valid_ratings = {"High", "Medium", "Low"}
    for row in rows:
        assert row["Impact"] in valid_ratings
        assert row["Influence"] in valid_ratings


def validate_documents() -> None:
    required = [
        "README.md",
        "docs/PROJECT_CONTEXT.md",
        "docs/PROJECT_INITIATION_DOCUMENT.md",
        "docs/STAKEHOLDER_MANAGEMENT.md",
        "docs/WBS_AND_SCHEDULE.md",
        "docs/RISK_MANAGEMENT.md",
        "docs/PROJECT_LEADERSHIP.md",
        "docs/METHODOLOGY_AND_CONTEXT.md",
        "docs/SOURCE_NOTES.md",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    assert not missing, f"Missing required documentation: {', '.join(missing)}"


def main() -> None:
    validate_gantt()
    validate_budget()
    validate_stakeholders()
    validate_documents()
    print("Portfolio validation passed: schedule, budget, stakeholders and docs are consistent.")


if __name__ == "__main__":
    main()
