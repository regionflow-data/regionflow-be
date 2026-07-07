from regionflow.events import cache_snapshots, publish_snapshots
from regionflow.pipeline import RegionSignal, build_region_snapshot
from regionflow.redshift import REGION_SIGNAL_SQL, dashboard_payload
from pathlib import Path


def main() -> None:
    snapshots = build_region_snapshot([RegionSignal("gangnam", 100, 12, 20)])
    assert snapshots[0].action == "rebalance-inventory"
    assert "mart_order_fulfillment" in REGION_SIGNAL_SQL
    assert dashboard_payload()["primaryMetric"] == "91.4%"
    assert callable(cache_snapshots)
    assert callable(publish_snapshots)
    pyproject = Path("pyproject.toml").read_text()
    assert "apache-airflow-providers-mysql" in pyproject
    assert "/api/dashboard" in Path("openapi.yaml").read_text()
    assert "mv_region_fulfillment_7d" in Path("sql/redshift_region_mart.sql").read_text()
    assert "pipeline_runs" in Path("sql/mysql_airflow_metadata.sql").read_text()
    for file in ["pyproject.toml", "openapi.yaml"]:
        assert "graphql" not in Path(file).read_text().lower(), f"graphql must not be used: {file}"
    print("regionflow-be_self_check_ok")


if __name__ == "__main__":
    main()
