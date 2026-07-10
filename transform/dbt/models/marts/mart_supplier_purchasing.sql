-- Supplier spend, on-time PO %, and cycle time. Required business-facing
-- terminus for the purchasing lineage (suppliers/purchase_orders/
-- purchase_order_items sources -> stg_* -> int_purchasing -> core -> here),
-- so purchasing data doesn't dead-end at the fact layer.
with po_agg as (
    select
        po.supplier_id,
        count(*) as total_pos,
        sum(case when po.status = 'received' then 1 else 0 end) as received_pos,
        round(100.0 * sum(case when po.expected_cycle_days <= s.lead_time_days then 1 else 0 end) / count(*), 1) as on_time_pct,
        round(avg(po.expected_cycle_days), 1) as avg_cycle_days
    from {{ ref('fct_purchase_orders') }} po
    left join {{ ref('dim_suppliers') }} s on po.supplier_id = s.supplier_id
    group by po.supplier_id
),

item_agg as (
    select
        supplier_id,
        sum(line_spend) as total_spend,
        sum(quantity) as total_units_ordered
    from {{ ref('fct_purchase_order_items') }}
    group by supplier_id
)

select
    sup.supplier_id,
    sup.supplier_name,
    sup.region_name,
    sup.lead_time_days,
    sup.reliability_score,
    coalesce(po.total_pos, 0) as total_pos,
    coalesce(po.received_pos, 0) as received_pos,
    po.on_time_pct,
    po.avg_cycle_days,
    coalesce(it.total_spend, 0) as total_spend,
    coalesce(it.total_units_ordered, 0) as total_units_ordered
from {{ ref('dim_suppliers') }} sup
left join po_agg po on sup.supplier_id = po.supplier_id
left join item_agg it on sup.supplier_id = it.supplier_id
order by total_spend desc
