create table if not exists mart_order_fulfillment (
  order_id varchar(64) encode zstd,
  region_code varchar(32) encode zstd,
  ordered_at timestamp encode az64,
  stockout_at timestamp encode az64,
  delivery_minutes int encode az64
)
diststyle key
distkey(region_code)
sortkey(ordered_at, region_code);

create materialized view if not exists mv_region_fulfillment_7d as
select
  region_code,
  count(*) as orders,
  sum(case when stockout_at is not null then 1 else 0 end) as stockouts,
  avg(delivery_minutes) as avg_delivery_minutes
from mart_order_fulfillment
where ordered_at >= current_date - interval '7 days'
group by 1;
