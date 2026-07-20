-- One row per controlled data-quality scenario (see data-generator/schema.md)
-- for demo storytelling: shows the pipeline surfaces known imperfections
-- rather than silently hiding them.
select 'duplicate_customer_rows' as scenario, count(*) - count(distinct customer_id) as row_count
from {{ source('raw', 'customers') }}

union all

select 'duplicate_order_rows', count(*) - count(distinct order_id)
from {{ source('raw', 'orders') }}

union all

select 'null_customer_email', count(*)
from {{ ref('stg_customers') }}
where email is null

union all

select 'null_order_promotion_id', count(*)
from {{ ref('stg_orders') }}
where promotion_id is null

union all

select 'invalid_order_status', count(*)
from {{ ref('stg_orders') }}
where status not in ('completed', 'cancelled', 'returned', 'pending')

union all

select 'late_arriving_orders', count(*)
from {{ ref('stg_orders') }}
where is_late_arriving

union all

select 'orphaned_order_item_product_fk', count(*)
from {{ ref('stg_order_items') }} oi
left join {{ ref('stg_products') }} p on oi.product_id = p.product_id
where p.product_id is null

union all

select 'in_transit_shipments', count(*)
from {{ ref('stg_shipments') }}
where ship_status = 'in_transit'

union all

select 'orphan_web_events', count(*)
from {{ ref('stg_web_events') }} e
left join {{ ref('stg_web_sessions') }} s on e.session_id = s.session_id
where s.session_id is null

union all

select 'dangling_po_item_product_fk', count(*)
from {{ ref('stg_purchase_order_items') }} poi
left join {{ ref('stg_products') }} p on poi.product_id = p.product_id
where p.product_id is null
