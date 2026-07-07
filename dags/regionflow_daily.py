from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag, task

from regionflow.events import cache_snapshots, publish_snapshots
from regionflow.pipeline import RegionSignal, RegionSnapshot, build_region_snapshot


@dag(
    dag_id="regionflow_daily",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["regionflow", "redshift"],
)
def regionflow_daily():
    @task
    def extract_signals() -> list[dict[str, int | str]]:
        return [
            {"region": "gangnam", "orders": 1200, "stockouts": 92, "delivery_minutes": 24},
            {"region": "mapo", "orders": 880, "stockouts": 31, "delivery_minutes": 21},
        ]

    @task
    def transform(rows: list[dict[str, int | str]]) -> list[dict[str, object]]:
        signals = [RegionSignal(**row) for row in rows]
        return [snapshot.__dict__ for snapshot in build_region_snapshot(signals)]

    @task
    def publish(rows: list[dict[str, object]]) -> dict[str, int]:
        snapshots = [RegionSnapshot(**row) for row in rows]
        return {"cached": cache_snapshots(snapshots), "published": publish_snapshots(snapshots)}

    publish(transform(extract_signals()))


regionflow_daily()
