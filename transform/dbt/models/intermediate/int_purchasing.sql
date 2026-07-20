-- product_id may be dangling (controlled orphan-FK scenario, see
-- stg_purchase_order_items) -- left join keeps the PO-item row visible with
-- null product attributes rather than dropping it.
select
    poi.po_item_id,
    poi.po_id,
    po.supplier_id,
    sup.supplier_name,
    sup.region_id as supplier_region_id,
    sup.lead_time_days as supplier_lead_time_days,
    sup.reliability_score,
    po.store_id,
    po.order_date,
    po.expected_date,
    po.status,
    date_diff('day', po.order_date::date, po.expected_date::date) as expected_cycle_days,
    poi.product_id,
    p.product_name,
    poi.quantity,
    poi.unit_cost,
    round(poi.quantity * poi.unit_cost, 2) as line_spend
from {{ ref('stg_purchase_order_items') }} poi
left join {{ ref('stg_purchase_orders') }} po on poi.po_id = po.po_id
left join {{ ref('stg_suppliers') }} sup on po.supplier_id = sup.supplier_id
left join {{ ref('stg_products') }} p on poi.product_id = p.product_id
