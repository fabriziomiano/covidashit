"""Serialization and formatting helpers for API responses."""

from __future__ import annotations

import datetime as dt
from decimal import Decimal
from typing import Any

def number(value: Any) -> str:
    """Format a count for dashboard cards."""

    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "n/a"


def display_date(value: Any) -> str:
    """Return a compact Italian-style date label for dashboard metadata."""

    if isinstance(value, dt.datetime):
        return value.strftime("%d/%m/%Y %H:%M")
    if isinstance(value, dt.date):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, str):
        try:
            return display_date(dt.datetime.fromisoformat(value))
        except ValueError:
            return value
    return str(value) if value is not None else "n/a"


def chart_date(value: Any) -> str:
    """Return a stable short label for chart categories."""

    if isinstance(value, dt.datetime):
        return value.strftime("%d %b '%y")
    if isinstance(value, dt.date):
        return value.strftime("%d %b '%y")
    return str(value)


def clean_document(value: Any) -> Any:
    """Recursively convert Python values into JSON-safe objects."""

    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, list):
        return [clean_document(item) for item in value]
    if isinstance(value, tuple):
        return [clean_document(item) for item in value]
    if isinstance(value, dict):
        return {str(key): clean_document(item) for key, item in value.items() if key != "_id"}
    return value
