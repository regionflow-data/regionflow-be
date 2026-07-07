from __future__ import annotations

import os
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def measured(operation: str, fn: Callable[[], T]) -> T:
    started_at = time.perf_counter()
    try:
        return fn()
    finally:
        elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)
        service = os.getenv("DATADOG_SERVICE", "regionflow-be")
        print(f"service={service} operation={operation} elapsedMs={elapsed_ms}")
