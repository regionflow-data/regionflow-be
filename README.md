# regionflow-be

RegionFlow Python backend for regional demand analytics.

## Stack

- Python, Airflow DAG, Redshift SQL boundary
- Redis snapshot cache
- RabbitMQ analytics event publishing

## Entry points

- `dags/regionflow_daily.py`
- `python -m regionflow.api`
- `GET /api/dashboard`

## Run

```bash
PYTHONPATH=src python -m regionflow.api
python -m pytest
```

See `requests.http` for sample payloads.

Contracts:
- `openapi.yaml`
- `sql/redshift_region_mart.sql`
