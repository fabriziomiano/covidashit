"""Tests for backend serialization helpers."""

from __future__ import annotations

import datetime as dt

from backend.app.services.serializers import chart_date, clean_document, display_date, number


def test_number_uses_italian_thousands_separator() -> None:
    """Counts are formatted for dashboard cards."""

    assert number(1234567) == "1.234.567"


def test_dates_are_displayed_in_dashboard_format() -> None:
    """Dashboard metadata dates stay compact and readable."""

    value = dt.datetime(2024, 1, 2, 15, 30)
    assert display_date(value) == "02/01/2024 15:30"
    assert chart_date(value) == "02 Jan '24"


def test_clean_document_removes_internal_id_and_serializes_dates() -> None:
    """Warehouse payloads are converted into JSON-safe dictionaries."""

    value = {"_id": "abc", "data": dt.date(2024, 1, 2), "items": [{"x": 1}]}
    assert clean_document(value) == {"data": "2024-01-02", "items": [{"x": 1}]}
