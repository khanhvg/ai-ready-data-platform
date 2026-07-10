-- On-time %, average lead time, and in-transit volume by carrier and region.
-- avg() skips nulls automatically, so in-transit shipments (null lead_time_days)
-- don't distort the average.
select
    sh.carrier,
    st.region_name,
    count(*) as shipment_count,
    sum(case when sh.is_on_time then 1 else 0 end) as on_time_count,
    round(100.0 * sum(case when sh.is_on_time then 1 else 0 end) / count(*), 1) as on_time_pct,
    round(avg(sh.lead_time_days), 1) as avg_lead_time_days,
    sum(case when sh.is_in_transit then 1 else 0 end) as in_transit_count
from {{ ref('fct_shipments') }} sh
inner join {{ ref('fct_orders') }} o on sh.order_id = o.order_id
inner join {{ ref('dim_stores') }} st on o.store_id = st.store_id
group by sh.carrier, st.region_name
order by st.region_name, sh.carrier
