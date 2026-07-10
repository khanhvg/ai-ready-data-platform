-- delivered_date is null on purpose for in-transit shipments (~8% rate,
-- see data-generator/schema.md) -- passed through unclean, not backfilled.
select
    shipment_id,
    order_id,
    carrier,
    ship_date,
    delivered_date,
    ship_status
from {{ source('raw', 'shipments') }}
