select
    shipment_id,
    order_id,
    carrier,
    ship_date,
    delivered_date,
    ship_status,
    lead_time_days,
    is_on_time,
    is_delayed,
    is_in_transit,
    is_returned
from {{ ref('int_fulfillment') }}
