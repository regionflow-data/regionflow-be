REGION_SIGNAL_SQL = """
select
  region_code as region,
  count(*) as orders,
  sum(case when stockout_at is not null then 1 else 0 end) as stockouts,
  avg(delivery_minutes) as delivery_minutes
from mart_order_fulfillment
where ordered_at >= current_date - interval '7 days'
group by 1
"""


def dashboard_payload() -> dict[str, object]:
    return {
        "title": "regional demand analytics",
        "primaryMetric": "91.4%",
        "secondaryMetric": "12 cohorts",
        "alerts": ["regional demand analytics", "12 cohorts"],
    }
